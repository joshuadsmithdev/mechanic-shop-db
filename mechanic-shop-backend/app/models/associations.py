# app/models/associations.py
from ..extensions import db

ticket_inventory = db.Table(
    "ticket_inventory",
    db.Column(
        "ticket_id",
        db.Integer,
        db.ForeignKey("service_ticket.ticket_id", ondelete="CASCADE"),
        primary_key=True,
    ),
    db.Column(
        "inventory_id",
        db.Integer,
        db.ForeignKey("inventory.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)
