from flask import Blueprint, request, jsonify, abort
from ...extensions import db
from ...models     import ServiceTicket, Mechanic, ServiceAssignment
from .schemas      import ServiceTicketSchema

tickets_bp       = Blueprint('service_tickets', __name__)
ticket_schema    = ServiceTicketSchema()
tickets_schema   = ServiceTicketSchema(many=True)

@tickets_bp.route('/', methods=['POST'])
def create_ticket():
    t = ticket_schema.load(request.get_json(), session=db.session)
    db.session.add(t)
    db.session.commit()
    return ticket_schema.jsonify(t), 201

@tickets_bp.route('/', methods=['GET'])
def list_tickets():
    allt = ServiceTicket.query.all()
    return tickets_schema.jsonify(allt)

@tickets_bp.route('/<int:ticket_id>/assign-mechanic/<int:mech_id>', methods=['PUT'])
def assign_mechanic(ticket_id, mech_id):
    print(f"Received ticket_id={ticket_id}, mech_id={mech_id}")

    # Check if ticket exists
    ticket = ServiceTicket.query.get(ticket_id)
    if not ticket:
        print("Ticket not found")
        return jsonify({"error": "Service ticket not found"}), 404

    # Check if mechanic exists
    mechanic = Mechanic.query.get(mech_id)
    if not mechanic:
        print("Mechanic not found")
        return jsonify({"error": "Mechanic not found"}), 404

    # Check if already assigned
    existing = ServiceAssignment.query.get((ticket_id, mech_id))
    if existing:
        print("Assignment already exists")
        return jsonify({"error": "Mechanic already assigned to this ticket"}), 400

    # Get optional hours from body
    data = request.get_json(silent=True) or {}
    hours = data.get("hours_worked", 0.0)
    print(f"Assigning with hours_worked={hours}")

    # Create assignment
    assignment = ServiceAssignment(
        service_ticket_id=ticket_id,
        mechanic_id=mech_id,
        hours_worked=hours
    )
    db.session.add(assignment)
    db.session.commit()

    return jsonify({
        "message": "Mechanic assigned successfully.",
        "ticket_id": ticket_id,
        "mechanic_id": mech_id,
        "hours_worked": float(hours)
    }), 201

    return jsonify({"message": f"Mechanic assigned {mech_id} to ticket {ticket_id}"}), 200

@tickets_bp.route('/<int:ticket_id>/remove-mechanic/<int:mech_id>', methods=['DELETE'])
def remove_mechanic(ticket_id, mech_id):
    assignment = ServiceAssignment.query.get_or_404((ticket_id, mech_id))
    db.session.delete(assignment)
    db.session.commit()
    return jsonify({"message": "Mechanic unassigned"}), 204
@tickets_bp.route('/<int:ticket_id>', methods=['PUT'])
def update_ticket(ticket_id):
    t = ServiceTicket.query.get_or_404(ticket_id)
    t = ticket_schema.load(request.get_json(), instance=t, session=db.session)
    db.session.commit()
    return ticket_schema.jsonify(t)
@tickets_bp.route('/<int:ticket_id>', methods=['GET'])
def get_ticket(ticket_id):
    t = ServiceTicket.query.get_or_404(ticket_id)
    return ticket_schema.jsonify(t)

@tickets_bp.route('/<int:ticket_id>/mechanics', methods=['GET'])
def get_ticket_mechanics(ticket_id):
    ticket = ServiceTicket.query.get_or_404(ticket_id)
    mechanics = [assignment.mechanic for assignment in ticket.assignments]
    from app.blueprints.mechanics.schemas import MechanicSchema
    return MechanicSchema(many=True).jsonify(mechanics)
@tickets_bp.route('/<int:ticket_id>', methods=['DELETE'])
def delete_ticket(ticket_id):
    ticket = ServiceTicket.query.get_or_404(ticket_id)
    db.session.delete(ticket)
    db.session.commit()
    return '', 204
