# app/models/inventory.py
from ..extensions import db
from .associations import ticket_inventory

class Inventory(db.Model):
    __tablename__ = "inventory"

    id    = db.Column(db.Integer, primary_key=True)
    name  = db.Column(db.String(128), nullable=False)
    price = db.Column(db.Float, nullable=False)

    service_tickets = db.relationship(
        "ServiceTicket",
        secondary=ticket_inventory,
        back_populates="parts",
    )
