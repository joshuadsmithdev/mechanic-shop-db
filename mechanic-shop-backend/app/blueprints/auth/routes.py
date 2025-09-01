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

def _validate_and_get_json():
    data = request.get_json(silent=True) or {}
    errors = login_schema.validate(data)
    if errors:
        return None, jsonify({"errors": errors}), 400
    return data, None, None

# ----------------------------------------------------
# Customer login → returns RAW JWT (no "Bearer " prefix)
# Support both /login and /auth/login for compatibility
# ----------------------------------------------------
@auth_bp.post("/login")
@auth_bp.post("/auth/login")
def login_customer():
    """
    Customer Login
    ---
    tags: [Auth]
    summary: Log in as a customer and receive a JWT
    description: Verifies customer credentials and returns a JWT. The response `token` is the raw JWT **without** the "Bearer " prefix.
    consumes:
      - application/json
    parameters:
      - in: body
        name: payload
        required: true
        schema:
          $ref: '#/definitions/LoginPayload'
    responses:
      200:
        description: JWT token
        schema:
          $ref: '#/definitions/TokenResponse'
        examples:
          application/json: {"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."}
      400:
        description: Bad request (validation error)
        schema:
          $ref: '#/definitions/Error'
      401:
        description: Invalid credentials
        schema:
          $ref: '#/definitions/Error'
    """
    data, err_resp, err_code = _validate_and_get_json()
    if err_resp:
        return err_resp, err_code

    user = Customer.query.filter_by(email=data["email"]).first()
    if not user or not user.check_password(data["password"]):
        return jsonify({"error": "Invalid email or password"}), 401

    uid = getattr(user, "customer_id", None) or getattr(user, "id")
    token = encode_token(uid, role="customer")
    return jsonify({"token": token}), 200


# ----------------------------------------------------
# Mechanic login → returns RAW JWT (no "Bearer " prefix)
# Support both /mechanics/login and /auth/mechanics/login
# ----------------------------------------------------
@auth_bp.post("/mechanics/login")
@auth_bp.post("/auth/mechanics/login")
def login_mechanic():
    """
    Mechanic Login
    ---
    tags: [Auth]
    summary: Log in as a mechanic and receive a JWT
    description: Verifies mechanic credentials and returns a JWT. The response `token` is the raw JWT **without** the "Bearer " prefix.
    consumes:
      - application/json
    parameters:
      - in: body
        name: payload
        required: true
        schema:
          $ref: '#/definitions/LoginPayload'
    responses:
      200:
        description: JWT token
        schema:
          $ref: '#/definitions/TokenResponse'
        examples:
          application/json: {"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."}
      400:
        description: Bad request (validation error)
        schema:
          $ref: '#/definitions/Error'
      401:
        description: Invalid credentials
        schema:
          $ref: '#/definitions/Error'
    """
    data, err_resp, err_code = _validate_and_get_json()
    if err_resp:
        return err_resp, err_code

    mech = Mechanic.query.filter_by(email=data["email"]).first()
    if not mech or not mech.check_password(data["password"]):
        return jsonify({"error": "Invalid email or password"}), 401

    mid = getattr(mech, "mechanic_id", None) or getattr(mech, "id")
    token = encode_token(mid, role="mechanic")
    return jsonify({"token": token}), 200
