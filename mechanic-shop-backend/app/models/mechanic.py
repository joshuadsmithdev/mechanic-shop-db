# app/models/mechanic.py
from ..extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class Mechanic(db.Model):
    __tablename__ = "mechanic"

    mechanic_id = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(100), nullable=False)
    email       = db.Column(db.String(100))
    phone       = db.Column(db.String(20))
    address     = db.Column(db.String(200))
    salary      = db.Column(db.Numeric(10, 2))
    password_hash = db.Column(db.String(512), nullable=True)

    # M↔M via ServiceAssignment
    assignments = db.relationship(
        "ServiceAssignment",
        back_populates="mechanic",
        cascade="all, delete-orphan",
    )
    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return bool(self.password_hash) and check_password_hash(self.password_hash, password)
