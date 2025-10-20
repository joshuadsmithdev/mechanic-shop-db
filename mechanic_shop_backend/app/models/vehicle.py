# app/models/vehicle.py
from ..extensions import db

class Vehicle(db.Model):
    __tablename__ = "vehicle"

    vin         = db.Column(db.String(17), primary_key=True)
    customer_id = db.Column(
        db.Integer,
        db.ForeignKey("customer.customer_id", ondelete="CASCADE"),
        nullable=False,
    )
    make          = db.Column(db.String(50))
    model         = db.Column(db.String(50))
    year          = db.Column(db.SmallInteger)
    license_plate = db.Column(db.String(15))

    owner = db.relationship("Customer", back_populates="vehicles")

    tickets = db.relationship(
        "ServiceTicket",
        back_populates="vehicle",
        cascade="all, delete-orphan",
    )
