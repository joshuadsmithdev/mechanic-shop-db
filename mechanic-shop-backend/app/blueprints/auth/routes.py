# app/blueprints/auth/routes.py
from flask import Blueprint, request, jsonify
from marshmallow import Schema, fields
from app.models import Customer, Mechanic
from app.utils.token import encode_token

auth_bp = Blueprint("auth", __name__)

class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)

login_schema = LoginSchema()

# -----------------------------
# Customer login -> returns JWT
# POST /login
# -----------------------------
@auth_bp.post("/login")
def login_customer():
    data = request.get_json(silent=True) or {}
    errors = login_schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400

    user = Customer.query.filter_by(email=data["email"]).first()
    if not user or not user.check_password(data["password"]):
        return jsonify({"error": "Invalid email or password"}), 401

    uid = getattr(user, "customer_id", None) or getattr(user, "id")
    return jsonify({"token": encode_token(uid, role="customer")}), 200


# -----------------------------
# Mechanic login -> returns JWT
# POST /mechanics/login
# -----------------------------
@auth_bp.post("/mechanics/login")
def login_mechanic():
    data = request.get_json(silent=True) or {}
    errors = login_schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400

    mech = Mechanic.query.filter_by(email=data["email"]).first()
    if not mech or not mech.check_password(data["password"]):
        return jsonify({"error": "Invalid email or password"}), 401

    mid = getattr(mech, "mechanic_id", None) or getattr(mech, "id")
    return jsonify({"token": encode_token(mid, role="mechanic")}), 200
