# app/blueprints/mechanics/routes.py
from flask import Blueprint, request, jsonify
from ...extensions import db
from ...models import Mechanic, ServiceAssignment
from .schemas import MechanicSchema

mechanics_bp       = Blueprint("mechanics", __name__)
mechanic_schema    = MechanicSchema()
mechanics_schema   = MechanicSchema(many=True)

# POST /mechanics  -> 201
@mechanics_bp.post("", strict_slashes=False)
def create_mechanic():
    data = request.get_json(silent=True) or {}

    # Handle password outside the schema
    password = data.pop("password", None)

    # Validate/load other fields via schema
    m = mechanic_schema.load(data, session=db.session)

    if password:
        # requires Mechanic.set_password on the model
        m.set_password(password)

    db.session.add(m)
    db.session.commit()
    return jsonify(mechanic_schema.dump(m)), 201


# GET /mechanics  -> 200
@mechanics_bp.get("", strict_slashes=False)
def list_mechanics():
    allm = Mechanic.query.all()
    return jsonify(mechanics_schema.dump(allm)), 200


# GET /mechanics/<id>  -> 200
@mechanics_bp.get("/<int:id>")
def get_mechanic(id):
    m = Mechanic.query.get_or_404(id)
    return jsonify(mechanic_schema.dump(m)), 200


# PUT /mechanics/<id>  -> 200
@mechanics_bp.put("/<int:id>")
def update_mechanic(id):
    m = Mechanic.query.get_or_404(id)
    data = request.get_json(silent=True) or {}

    # Pull password out (schema shouldn’t see it)
    password = data.pop("password", None)

    # Partial update for other fields
    m = mechanic_schema.load(data, instance=m, partial=True, session=db.session)

    if password:
        m.set_password(password)

    db.session.commit()
    return jsonify(mechanic_schema.dump(m)), 200


# DELETE /mechanics/<id>  -> 204
@mechanics_bp.delete("/<int:id>")
def delete_mechanic(id):
    m = Mechanic.query.get_or_404(id)
    db.session.delete(m)
    db.session.commit()
    return "", 204


# GET /mechanics/ranked  -> 200
@mechanics_bp.get("/ranked")
def get_ranked_mechanics():
    # Example: order by number of assignments (desc)
    ranked = (
        db.session.query(
            Mechanic,
            db.func.count(ServiceAssignment.mechanic_id).label("assignment_count"),
        )
        .outerjoin(ServiceAssignment, Mechanic.mechanic_id == ServiceAssignment.mechanic_id)
        .group_by(Mechanic.mechanic_id)
        .order_by(db.desc("assignment_count"))
        .all()
    )

    result = [
        {"mechanic": mechanic_schema.dump(mech), "assignment_count": count}
        for mech, count in ranked
    ]
    return jsonify(result), 200
