# app/models/service_ticket.py
from ..extensions import db
from .associations import ticket_inventory

class ServiceTicket(db.Model):
    __tablename__ = "service_ticket"

    ticket_id   = db.Column(db.Integer, primary_key=True)
    vin         = db.Column(
        db.String(17),
        db.ForeignKey("vehicle.vin", ondelete="CASCADE"),
        nullable=False,
    )
    date_in     = db.Column(db.DateTime, server_default=db.func.now())
    date_out    = db.Column(db.DateTime)
    description = db.Column(db.Text)
    status      = db.Column(
        db.Enum("open", "in_progress", "closed", name="ticket_status_enum"),
        default="open",
        nullable=False,
    )
    total_cost  = db.Column(db.Numeric(10, 2), default=0.00)

    vehicle = db.relationship("Vehicle", back_populates="tickets")

    assignments = db.relationship(
        "ServiceAssignment",
        back_populates="ticket",
        cascade="all, delete-orphan",
    )

    # M2M with Inventory via association table
    parts = db.relationship(
        "Inventory",
        secondary=ticket_inventory,
        back_populates="service_tickets",
    )
