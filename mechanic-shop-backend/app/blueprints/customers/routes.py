from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Customer
from .schemas import CustomerSchema
from app.extensions import limiter
from app.utils.token import encode_token, token_required
from .schemas import LoginSchema
login_schema = LoginSchema()

customers_bp = Blueprint("customers", __name__)

customer_schema = CustomerSchema()
customer_list_schema = CustomerSchema(many=True)

# Create a new customer
@customers_bp.route("/customers", methods=["POST"])
@limiter.limit("10 per minute")  # Rate limit to prevent abuse
def create_customer():
    data = request.get_json()
    try:
        customer = customer_schema.load(data)
        customer.set_password(data.get('password'))  # Hash the password
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    db.session.add(customer)
    db.session.commit()
    return customer_schema.jsonify(customer), 201

# Login route to get token
@customers_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    try:
        creds = login_schema.load(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    customer = Customer.query.filter_by(email=creds['email']).first()
    if customer and customer.check_password(creds['password']):
        token = encode_token(customer.customer_id)
        return jsonify({"token": token}), 200
    else:
        return jsonify({"error": "Invalid email or password"}), 401

# Get all customers
@customers_bp.route("/customers", methods=["GET"])
@limiter.limit("100 per hour")  # Rate limit for read operations
def get_customers():
   # Get query parameters ?page=1&per_page=10
    page = request.args.get("page", 1, type=int)
    per_page = min(request.args.get("per_page", 10, type=int), 50)  # Optional: max 50 per page

# Paginate query
    paginated = Customer.query.paginate(page=page, per_page=per_page, error_out=False)

# Return structured pagination response
    return jsonify({
        "total": paginated.total,
        "pages": paginated.pages,
        "current_page": paginated.page,
        "per_page": paginated.per_page,
        "data": customer_list_schema.dump(paginated.items)
    }), 200


# Get a customer by ID
@customers_bp.route("/customers/<int:customer_id>", methods=["GET"])
def get_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    return customer_schema.jsonify(customer), 200

# Update a customer
@customers_bp.route("/customers/<int:customer_id>", methods=["PUT"])
def update_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    data = request.get_json()

    try:
        updated_customer = customer_schema.load(data, instance=customer, partial=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    db.session.commit()
    return customer_schema.jsonify(updated_customer), 200

# Delete a customer
@customers_bp.route("/customers/<int:customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": "Customer deleted"}), 204
