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
    t = ServiceTicket.query.get_or_404(ticket_id)
    m = Mechanic.query.get_or_404(mech_id)
    existing = ServiceAssignment.query.get((ticket_id, mech_id))
    if existing:
        return jsonify({"error": "Mechanic already assigned to this ticket"}), 400
    hours = request.get_json(silent=True).get('hours', 0)
    hours_worked = hours.get('hours_worked', 0.00)
    assignment = ServiceAssignment(
        service_ticket_id=ticket_id,
        mechanic_id=mech_id,
        hours_worked=hours_worked
    )
    db.session.add(assignment)
    db.session.commit()
    return ticket_schema.jsonify(t)

@tickets_bp.route('/<int:ticket_id>/remove-mechanic/<int:mech_id>', methods=['PUT'])
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
