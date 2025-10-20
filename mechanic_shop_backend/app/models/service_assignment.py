# app/models/service_assignment.py
from ..extensions import db

class ServiceAssignment(db.Model):
    __tablename__ = "service_assignment"

    service_ticket_id = db.Column(
        db.Integer,
        db.ForeignKey("service_ticket.ticket_id", ondelete="CASCADE"),
        primary_key=True,
    )
    mechanic_id = db.Column(
        db.Integer,
        db.ForeignKey("mechanic.mechanic_id", ondelete="CASCADE"),
        primary_key=True,
    )
    hours_worked = db.Column(db.Numeric(5, 2), default=0.00)

    ticket   = db.relationship("ServiceTicket", back_populates="assignments")
    mechanic = db.relationship("Mechanic",      back_populates="assignments")
