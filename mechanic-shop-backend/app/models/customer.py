# app/models/customer.py
from ..extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class Customer(db.Model):
    __tablename__ = "customer"

    customer_id   = db.Column(db.Integer, primary_key=True)
    first_name    = db.Column(db.String(100), nullable=False)
    last_name     = db.Column(db.String(100), nullable=False)
    phone         = db.Column(db.String(20))
    email         = db.Column(db.String(120), unique=True, nullable=False)
    address       = db.Column(db.String(200))
    password_hash = db.Column(db.String(512), nullable=False)

    # 1→M: customer → vehicles
    vehicles = db.relationship(
        "Vehicle",
        back_populates="owner",
        cascade="all, delete-orphan",
    )

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)
