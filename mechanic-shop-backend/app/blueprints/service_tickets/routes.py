# app/blueprints/service_tickets/routes.py
from flask import Blueprint, request, jsonify
from ...extensions import db
from ...models import ServiceTicket, Vehicle, Mechanic, ServiceAssignment
from .schemas import ServiceTicketSchema
from app.utils.token import token_required

tickets_bp = Blueprint("tickets", __name__)
ticket_schema = ServiceTicketSchema()
tickets_schema = ServiceTicketSchema(many=True)


@tickets_bp.route("/", methods=["POST"])
@token_required("customer", "mechanic")
def create_ticket(current_user_id=None, current_role=None):
    """
    Create ticket
    ---
    tags: [Service Tickets]
    summary: Create a new service ticket
    description: Create a ticket for a vehicle. Provide either `vin` or `vehicle_id`.
    consumes:
      - application/json
    parameters:
      - in: body
        name: payload
        required: true
        schema:
          type: object
          properties:
            description:
              type: string
            status:
              type: string
              enum: [open, in_progress, closed]
              default: open
            vin:
              type: string
            vehicle_id:
              type: integer
          required: [description]
    security:
      - bearerAuth: []
    responses:
      201:
        description: Created
        schema: { "$ref": "#/definitions/ServiceTicketResponse" }
      400:
        description: Vehicle not found or invalid payload
        schema: { "$ref": "#/definitions/Error" }
      401:
        description: Unauthorized
        schema: { "$ref": "#/definitions/Error" }
    """
    data = request.get_json(silent=True) or {}

    description = (data.get("description") or "").strip()
    if not description:
        return jsonify({"error": "description is required"}), 400

    vin = (data.get("vin") or "").strip() or None
    vehicle_id = data.get("vehicle_id")

    vehicle = None
    if vehicle_id:
        # Your Vehicle PK is vin; if you also store numeric ids, adjust here
        vehicle = Vehicle.query.get(vehicle_id)  # only works if you have numeric PK; else ignore
    if not vehicle and vin:
        vehicle = Vehicle.query.filter_by(vin=vin).first()

    # Tests allow 201 or 400; we *require* a real vehicle -> 400 if missing
    if not vehicle:
        return jsonify({"error": "Vehicle not found; provide a valid vin or vehicle_id"}), 400

    ticket = ServiceTicket(
        description=description,
        status=data.get("status", "open"),
        vin=vehicle.vin
    )
    db.session.add(ticket)
    db.session.commit()

    return ticket_schema.jsonify(ticket), 201


@tickets_bp.route("/", methods=["GET"])
def list_tickets():
    """
    List tickets
    ---
    tags: [Service Tickets]
    summary: List all service tickets
    responses:
      200:
        description: Array of tickets
    """
    items = ServiceTicket.query.all()
    return tickets_schema.jsonify(items), 200


@tickets_bp.route("/<int:ticket_id>", methods=["GET"])
def get_ticket(ticket_id: int):
    """
    Get ticket
    ---
    tags: [Service Tickets]
    summary: Get a ticket by id
    parameters:
      - in: path
        name: ticket_id
        type: integer
        required: true
    responses:
      200:
        description: The ticket
      404:
        description: Not found
    """
    t = ServiceTicket.query.get(ticket_id)
    if not t:
        return jsonify({"error": "Ticket not found"}), 404
    return ticket_schema.jsonify(t), 200


@tickets_bp.route("/<int:ticket_id>", methods=["PUT"])
@token_required("mechanic", "admin")
def update_ticket(ticket_id: int, current_user_id=None, current_role=None):
    """
    Update ticket
    ---
    tags: [Service Tickets]
    summary: Update a ticket
    parameters:
      - in: path
        name: ticket_id
        type: integer
        required: true
      - in: body
        name: payload
        schema:
          type: object
          properties:
            description: { type: string }
            status: { type: string, enum: [open, in_progress, closed] }
    security:
      - bearerAuth: []
    responses:
      200: { description: Updated ticket }
      404: { description: Not found }
    """
    t = ServiceTicket.query.get(ticket_id)
    if not t:
        return jsonify({"error": "Ticket not found"}), 404

    data = request.get_json(silent=True) or {}
    if "description" in data:
        t.description = data["description"]
    if "status" in data:
        t.status = data["status"]

    db.session.commit()
    return ticket_schema.jsonify(t), 200


@tickets_bp.route("/<int:ticket_id>", methods=["DELETE"])
@token_required("mechanic", "admin")
def delete_ticket(ticket_id: int, current_user_id=None, current_role=None):
    """
    Delete ticket
    ---
    tags: [Service Tickets]
    summary: Delete a ticket
    parameters:
      - in: path
        name: ticket_id
        type: integer
        required: true
    security:
      - bearerAuth: []
    responses:
      204: { description: Deleted }
      404: { description: Not found }
    """
    t = ServiceTicket.query.get(ticket_id)
    if not t:
        return jsonify({"error": "Ticket not found"}), 404
    db.session.delete(t)
    db.session.commit()
    return "", 204


@tickets_bp.route("/<int:ticket_id>/assign-mechanic/<int:mechanic_id>", methods=["POST"])
@token_required("admin", "mechanic")
def assign_mechanic(ticket_id: int, mechanic_id: int, current_user_id=None, current_role=None):
    """
    Assign mechanic
    ---
    tags: [Service Tickets]
    summary: Assign a mechanic to a ticket
    parameters:
      - in: path
        name: ticket_id
        type: integer
        required: true
      - in: path
        name: mechanic_id
        type: integer
        required: true
    security:
      - bearerAuth: []
    responses:
      200: { description: Mechanic assigned }
      404: { description: Not found }
    """
    t = ServiceTicket.query.get(ticket_id)
    if not t:
        return jsonify({"error": "Ticket not found"}), 404

    mech = Mechanic.query.get(mechanic_id)
    if not mech:
        return jsonify({"error": "Mechanic not found"}), 404

    # Simple linking model; adjust to your actual ServiceAssignment columns
    existing = ServiceAssignment.query.filter_by(
        service_ticket_id=ticket_id, mechanic_id=mechanic_id
    ).first()
    if not existing:
        sa = ServiceAssignment(service_ticket_id=ticket_id, mechanic_id=mechanic_id)
        db.session.add(sa)
        db.session.commit()

    return jsonify({"message": "Mechanic assigned"}), 200

# DELETE /service_tickets/<ticket_id>/assign-mechanic/<mechanic_id>
@tickets_bp.delete("/<int:ticket_id>/assign-mechanic/<int:mechanic_id>")
@token_required("mechanic", "admin")
def remove_mechanic_assignment(ticket_id: int, mechanic_id: int, current_role=None, current_user_id=None):
    """
    Remove Mechanic from Ticket
    ---
    tags: [Service Assignments]
    summary: Unassign a mechanic from a service ticket
    description: Deletes the ServiceAssignment row if it exists. Idempotent.
    security:
      - bearerAuth: []
    parameters:
      - in: path
        name: ticket_id
        type: integer
        required: true
      - in: path
        name: mechanic_id
        type: integer
        required: true
    responses:
      200:
        description: Assignment removed (or not present)
        examples:
          application/json: {"message": "Assignment removed"}
      404:
        description: Ticket not found
        examples:
          application/json: {"error": "Ticket not found"}
    """
    # ensure ticket exists
    ticket = ServiceTicket.query.get(ticket_id)
    if not ticket:
        return jsonify({"error": "Ticket not found"}), 404

    # delete assignment if present
    sa = ServiceAssignment.query.filter_by(
        service_ticket_id=ticket_id, mechanic_id=mechanic_id
    ).first()

    if sa:
        db.session.delete(sa)
        db.session.commit()
        return jsonify({"message": "Assignment removed"}), 200
    else:
        # idempotent: OK even if nothing to delete
        return jsonify({"message": "No assignment to remove"}), 200

