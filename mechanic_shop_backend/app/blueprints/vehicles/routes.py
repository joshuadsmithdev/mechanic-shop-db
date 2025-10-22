from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Vehicle, Customer
from .schemas import VehicleSchema

vehicles_bp = Blueprint("vehicles", __name__)

vehicle_schema = VehicleSchema()
vehicle_list_schema = VehicleSchema(many=True)

# With url_prefix="/api/vehicles", these become /api/vehicles/...
@vehicles_bp.route("/", methods=["POST"])
def create_vehicle():
    data = request.get_json() or {}
    customer = Customer.query.get(data.get("customer_id"))
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    try:
        vehicle = vehicle_schema.load(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    db.session.add(vehicle)
    db.session.commit()
    return vehicle_schema.jsonify(vehicle), 201

@vehicles_bp.route("/", methods=["GET"])
def get_vehicles():
    vehicles = Vehicle.query.all()
    return vehicle_list_schema.jsonify(vehicles), 200

@vehicles_bp.route("/<string:vin>", methods=["GET"])
def get_vehicle(vin):
    vehicle = Vehicle.query.get_or_404(vin)
    return vehicle_schema.jsonify(vehicle), 200

@vehicles_bp.route("/<string:vin>", methods=["PUT"])
def update_vehicle(vin):
    vehicle = Vehicle.query.get_or_404(vin)
    data = request.get_json() or {}
    try:
        updated = vehicle_schema.load(data, instance=vehicle, partial=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    db.session.commit()
    return vehicle_schema.jsonify(updated), 200

@vehicles_bp.route("/<string:vin>", methods=["DELETE"])
def delete_vehicle(vin):
    vehicle = Vehicle.query.get_or_404(vin)
    db.session.delete(vehicle)
    db.session.commit()
    # 204 must not return a body
    return ("", 204)

# keep this helper under /api/customers/<id>/vehicles (mounted in customers bp or stay here)
@vehicles_bp.route("/by_customer/<int:customer_id>", methods=["GET"])
def get_customer_vehicles_by_query(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    return vehicle_list_schema.jsonify(customer.vehicles), 200
