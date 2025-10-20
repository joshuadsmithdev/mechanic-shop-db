# app/blueprints/mechanics/mechanic_ticket_routes.py
from flask import Blueprint, jsonify
from ...extensions import db
from ...models import ServiceTicket, ServiceAssignment
from ...utils.token import token_required

mechanic_ticket_bp = Blueprint("mechanic_ticket", __name__)

@mechanic_ticket_bp.get("/my-assigned-tickets")
@token_required("mechanic", "admin")
def get_my_assigned_tickets(current_user_id=None, current_role=None):
    """
    Get My Assigned Tickets
    ---
    tags: [Mechanics]
    summary: List tickets assigned to the logged-in mechanic
    description: Returns all service tickets assigned to the authenticated mechanic (based on JWT `sub`).
    security:
      - bearerAuth: []
    responses:
      200:
        description: List of tickets
        schema:
          type: array
          items:
            type: object
            properties:
              id: { type: integer, example: 1 }
              vin: { type: string, example: "1ABCDEF2345678901" }
              description: { type: string, example: "Brake pad replacement" }
              status: { type: string, example: "open" }
              date_in: { type: string, example: "2025-08-31T12:34:56" }
              date_out: { type: string, nullable: true, example: null }
              total_cost: { type: string, example: "0.00" }
      401:
        description: Missing/invalid token
        schema:
          type: object
          properties:
            error: { type: string, example: "Missing or invalid Authorization header" }
    """
    # The token_required decorator will pass JWT "sub" here when we include this arg
    if not current_user_id:
        return jsonify({"error": "Unable to determine mechanic from token"}), 400

    try:
        mechanic_id = int(current_user_id)
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid mechanic id in token"}), 400

    tickets = (
        db.session.query(ServiceTicket)
        .join(
            ServiceAssignment,
            ServiceAssignment.service_ticket_id == ServiceTicket.ticket_id,
        )
        .filter(ServiceAssignment.mechanic_id == mechanic_id)
        .all()
    )

    payload = []
    for t in tickets:
        payload.append({
            "id": getattr(t, "ticket_id", None) or getattr(t, "id", None),
            "vin": t.vin,
            "description": t.description,
            "status": t.status,
            "date_in": t.date_in.isoformat() if getattr(t, "date_in", None) else None,
            "date_out": t.date_out.isoformat() if getattr(t, "date_out", None) else None,
            "total_cost": str(getattr(t, "total_cost", "0.00")),
        })

    return jsonify(payload), 200
