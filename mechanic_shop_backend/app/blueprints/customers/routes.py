# app/blueprints/customers/routes.py
from flask import Blueprint, request, jsonify
from app.extensions import db, limiter
from app.models import Customer
from .schemas import CustomerSchema

customers_bp = Blueprint("customers", __name__)

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)

# GET /api/customers  and  /api/customers/
@customers_bp.get("", strict_slashes=False)
@customers_bp.get("/", strict_slashes=False)
@limiter.limit("100 per hour")
def list_customers():
    customers = Customer.query.all()
    return jsonify(customers_schema.dump(customers)), 200

# POST /api/customers  and  /api/customers/
@customers_bp.post("", strict_slashes=False)
@customers_bp.post("/", strict_slashes=False)
@limiter.limit("10 per minute")
def create_customer():
    data = request.get_json() or {}
    # Validate & load via marshmallow (uses session for nested/unique checks if any)
    customer = customer_schema.load(data, session=db.session)

    # Optional: set password if provided
    if "password" in data and data["password"]:
        customer.set_password(data["password"])

    db.session.add(customer)
    db.session.commit()
    return jsonify(customer_schema.dump(customer)), 201

# GET /api/customers/<id>
@customers_bp.get("/<int:customer_id>")
def get_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    return jsonify(customer_schema.dump(customer)), 200

# PUT /api/customers/<id>  (partial allowed via marshmallow)
@customers_bp.put("/<int:customer_id>")
def update_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    data = request.get_json() or {}
    try:
        updated = customer_schema.load(
            data,
            instance=customer,
            partial=True,         # allow partial updates
            session=db.session
        )
    except Exception as e:
        # e.g., invalid email format, unique violations surfaced via schema, etc.
        return jsonify({"error": str(e)}), 400

    db.session.commit()
    return jsonify(customer_schema.dump(updated)), 200

# DELETE /api/customers/<id>
@customers_bp.delete("/<int:customer_id>")
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    db.session.delete(customer)
    db.session.commit()
    return "", 204
