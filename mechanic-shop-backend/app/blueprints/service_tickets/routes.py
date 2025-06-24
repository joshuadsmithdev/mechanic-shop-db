from flask import Blueprint, request, jsonify, abort
from ...extensions import db
from ...models     import ServiceTicket, Mechanic
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
    t.assignments.append(m)
    db.session.commit()
    return ticket_schema.jsonify(t)

@tickets_bp.route('/<int:ticket_id>/remove-mechanic/<int:mech_id>', methods=['PUT'])
def remove_mechanic(ticket_id, mech_id):
    t = ServiceTicket.query.get_or_404(ticket_id)
    m = Mechanic.query.get_or_404(mech_id)
    t.assignments.remove(m)
    db.session.commit()
    return ticket_schema.jsonify(t)
