from flask import Blueprint, request, jsonify, abort
from ...extensions import db
from ...models import Inventory
from .schemas import InventorySchema

inventory_bp = Blueprint('inventory', __name__)
inventory_schema = InventorySchema()
inventories_schema = InventorySchema(many=True)

@inventory_bp.route('/', methods=['POST'])
def create_inventory():
    data = request.get_json()
    part = inventory_schema.load(data, session=db.session)
    db.session.add(part)
    db.session.commit()
    return inventory_schema.jsonify(part), 201

@inventory_bp.route('/', methods=['GET'])
def list_inventory():
    parts = Inventory.query.all()
    return inventories_schema.jsonify(parts), 200

@inventory_bp.route('/<int:id>', methods=['GET'])
def get_inventory(id):
    part = Inventory.query.get_or_404(id)
    return inventory_schema.jsonify(part)

@inventory_bp.route('/<int:id>', methods=['PUT'])
def update_inventory(id):
    part = Inventory.query.get_or_404(id)
    data = inventory_schema.load(request.get_json(), instance=part, session=db.session)
    db.session.commit()
    return inventory_schema.jsonify(part)

@inventory_bp.route('/<int:id>', methods=['DELETE'])
def delete_inventory(id):
    part = Inventory.query.get_or_404(id)
    db.session.delete(part)
    db.session.commit()
    return '', 204
@inventory_bp.route('/search', methods=['GET'])
def search_inventory():
    query = request.args.get('q', '')
    if not query:
        return jsonify({"message": "Query parameter 'q' is required."}), 400

    parts = Inventory.query.filter(
        (Inventory.name.ilike(f'%{query}%')) |
        (Inventory.description.ilike(f'%{query}%'))
    ).all()

    return inventories_schema.jsonify(parts), 200
