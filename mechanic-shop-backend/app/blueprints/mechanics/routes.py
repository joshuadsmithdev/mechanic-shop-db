from flask import Blueprint, request, jsonify, abort
from ...extensions import db
from ...models     import Mechanic
from .schemas      import MechanicSchema

mechanics_bp      = Blueprint('mechanics', __name__)
mechanic_schema  = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)

@mechanics_bp.route('/', methods=['POST'])
def create_mechanic():
    data = request.get_json()
    m = mechanic_schema.load(data, session=db.session)
    db.session.add(m)
    db.session.commit()
    return mechanic_schema.jsonify(m), 201

@mechanics_bp.route('/', methods=['GET'])
def list_mechanics():
    allm = Mechanic.query.all()
    return mechanics_schema.jsonify(allm)

@mechanics_bp.route('/<int:id>', methods=['PUT'])
def update_mechanic(id):
    m = Mechanic.query.get_or_404(id)
    m = mechanic_schema.load(request.get_json(), instance=m, session=db.session)
    db.session.commit()
    return mechanic_schema.jsonify(m)

@mechanics_bp.route('/<int:id>', methods=['DELETE'])
def delete_mechanic(id):
    m = Mechanic.query.get_or_404(id)
    db.session.delete(m)
    db.session.commit()
    return '', 204
