# app/blueprints/customers/ticket_routes.py
from flask import Blueprint, jsonify
from ...extensions import db
from ...models import ServiceTicket, Vehicle
from ...utils.token import token_required
from ..service_tickets.schemas import ServiceTicketSchema

customer_ticket_bp = Blueprint("customer_tickets", __name__)
tickets_schema = ServiceTicketSchema(many=True)

@customer_ticket_bp.get("/my-tickets")
@token_required("customer")  # decorator factory -> must have parentheses
def get_my_tickets(current_user_id=None, current_role=None):
    """
    Get my tickets
    ---
    tags: [Customer-Protected]
    summary: List tickets for the authenticated customer
    security:
      - bearerAuth: []
    responses:
      200:
        description: List of tickets for the current customer
      401:
        description: Unauthorized / invalid token
    """
    # token_required puts the JWT "sub" here
    try:
        cid = int(current_user_id)
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid token"}), 401

    tickets = (
        db.session.query(ServiceTicket)
        .join(Vehicle, ServiceTicket.vin == Vehicle.vin)
        .filter(Vehicle.customer_id == cid)
        .all()
    )

    # Use Marshmallow dump + Flask jsonify for portability
    return jsonify(tickets_schema.dump(tickets)), 200
