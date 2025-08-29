# app/blueprints/service_tickets/routes.py
from flask import Blueprint, request, jsonify, url_for
from ...extensions import db
from app.models.service_ticket import ServiceTicket
from app.models.mechanic import Mechanic
from app.models.service_assignment import ServiceAssignment
from app.models.inventory import Inventory
from app.models.vehicle import Vehicle
from .schemas import ServiceTicketSchema
from app.utils.token import token_required  # encode_token not needed here

tickets_bp     = Blueprint("service_tickets", __name__)
ticket_schema  = ServiceTicketSchema()
tickets_schema = ServiceTicketSchema(many=True)


def _normalize_vin(data: dict) -> None:
    """Strip Postman-style {{VIN}} braces if present."""
    vin = data.get("vin")
    if isinstance(vin, str) and vin.startswith("{{") and vin.endswith("}}"):
        data["vin"] = vin[2:-2]


# POST /service_tickets  (auth required) -> 201
@tickets_bp.post("", strict_slashes=False)
@token_required
def create_ticket(current_customer_id):
    data = request.get_json(silent=True) or {}
    data.setdefault("customer_id", current_customer_id)
    _normalize_vin(data)

    vehicle_id = data.get("vehicle_id")
    vin = data.get("vin")

    if not (vehicle_id or vin):
        return jsonify({"error": "Either vehicle_id or vin must be provided"}), 400

    if vehicle_id and not vin:
        v = Vehicle.query.get(vehicle_id)
        if not v:
            return jsonify({"error": f"Vehicle with id {vehicle_id} not found"}), 404
        data["vin"] = v.vin

    try:
        t = ticket_schema.load(data, session=db.session)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    db.session.add(t)
    db.session.commit()

    resp = jsonify(ticket_schema.dump(t))
    resp.status_code = 201
    # Canonical Location header to GET endpoint
    resp.headers["Location"] = url_for("service_tickets.get_ticket", ticket_id=t.ticket_id)
    return resp


# GET /service_tickets  (auth required) -> 200
@tickets_bp.get("", strict_slashes=False)
@token_required
def list_tickets(_current_customer_id):
    allt = ServiceTicket.query.all()
    return jsonify(tickets_schema.dump(allt)), 200


# GET /service_tickets/<id> (auth required) -> 200
@tickets_bp.get("/<int:ticket_id>")
@token_required
def get_ticket(current_customer_id, ticket_id):
    t = ServiceTicket.query.get_or_404(ticket_id)
    return jsonify(ticket_schema.dump(t)), 200


# PUT /service_tickets/<id> (auth required) -> 200
# Supports add/remove mechanic IDs in the same payload if your tests send them.
@tickets_bp.put("/<int:ticket_id>")
@token_required
def update_ticket(current_user, ticket_id):
    t = ServiceTicket.query.get_or_404(ticket_id)
    data = (request.get_json(silent=True) or {}).copy()

    add_ids = data.pop("add_ids", [])
    remove_ids = data.pop("remove_ids", [])

    # Update core fields (partial)
    try:
        t = ticket_schema.load(data, instance=t, partial=True, session=db.session)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    # Maintain mechanic assignments (use filter_by, safer than .get on composite)
    for mid in add_ids:
        existing = ServiceAssignment.query.filter_by(
            service_ticket_id=ticket_id, mechanic_id=mid
        ).first()
        if not existing:
            db.session.add(
                ServiceAssignment(service_ticket_id=ticket_id, mechanic_id=mid, hours_worked=0.0)
            )

    for mid in remove_ids:
        existing = ServiceAssignment.query.filter_by(
            service_ticket_id=ticket_id, mechanic_id=mid
        ).first()
        if existing:
            db.session.delete(existing)

    db.session.commit()
    return jsonify(ticket_schema.dump(t)), 200


# POST /service_tickets/<id>/assign (auth required) -> 200
# Body: {"mechanic_ids": [], "inventory_ids": []}
@tickets_bp.post("/<int:ticket_id>/assign-mechanic/<int:mechanic_id>")
@token_required
def assign_single_mechanic(current_user, ticket_id, mechanic_id):
    t = ServiceTicket.query.get_or_404(ticket_id)
    mech = Mechanic.query.get_or_404(mechanic_id)

    existing = ServiceAssignment.query.filter_by(
        service_ticket_id=ticket_id, mechanic_id=mechanic_id
    ).first()
    data = request.get_json(silent=True) or {}
    mech_ids = data.get("mechanic_ids", [])
    inv_ids  = data.get("inventory_ids", [])

    # Attach mechanics (via join table)
    for mid in mech_ids:
        existing = ServiceAssignment.query.filter_by(
            service_ticket_id=ticket_id, mechanic_id=mid
        ).first()
        if not existing:
            db.session.add(
                ServiceAssignment(service_ticket_id=ticket_id, mechanic_id=mechanic_id, hours_worked=0.0)
            )

    # Attach inventory parts (many-to-many)
    if hasattr(t, "parts"):
        for pid in inv_ids:
            part = Inventory.query.get(pid)
            if part and part not in t.parts:
                t.parts.append(part)

    db.session.commit()
    return jsonify(ticket_schema.dump(t)), 200


# DELETE /service_tickets/<int:ticket_id> (auth required) -> 204
@tickets_bp.delete("/<int:ticket_id>")
@token_required
def delete_ticket(current_user, ticket_id):
    t = ServiceTicket.query.get_or_404(ticket_id)
    db.session.delete(t)
    db.session.commit()
    return "", 204

# app/blueprints/service_tickets/routes.py

@tickets_bp.delete("/<int:ticket_id>/assign-mechanic/<int:mechanic_id>")
@token_required  # or @token_required("mechanic","admin")
def remove_mechanic_from_ticket(current_user, ticket_id, mechanic_id):
    # Ensure ticket exists (keeps 404 for nonexistent ticket ids)
    ServiceTicket.query.get_or_404(ticket_id)

    assignment = ServiceAssignment.query.filter_by(
        service_ticket_id=ticket_id,
        mechanic_id=mechanic_id
    ).first()

    if assignment:
        db.session.delete(assignment)
        db.session.commit()
    else:
        # nothing to delete; keep the operation idempotent
        db.session.rollback()

    return "", 204
