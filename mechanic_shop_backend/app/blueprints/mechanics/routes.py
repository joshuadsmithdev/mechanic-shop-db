# app/blueprints/mechanics/routes.py
from flask import Blueprint, request, jsonify
from ...extensions import db
from ...models import Mechanic, ServiceAssignment
from .schemas import MechanicSchema
from marshmallow import ValidationError

mechanics_bp       = Blueprint("mechanics", __name__)
mechanic_schema    = MechanicSchema()
mechanics_schema   = MechanicSchema(many=True)

# POST /mechanics  -> 201
@mechanics_bp.route('/', methods=['POST'])
def create_mechanic():
    """
    Create Mechanic
    ---
    tags: [Mechanics]
    summary: Create a new mechanic
    description: >
      Creates a mechanic record. **name** and **email** are required.
      Optionally include **password** to set the login password (it will be hashed).
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: payload
        required: true
        schema:
          $ref: '#/definitions/MechanicPayload'
    responses:
      201:
        description: Created mechanic
        schema:
          $ref: '#/definitions/Mechanic'
        examples:
          application/json:
            mechanic_id: 1
            name: "Sam Wrench"
            email: "sam@example.com"
            phone: "555-1111"
            salary: "0.00"
            address: "123 Main St"
      400:
        description: Validation error
        schema:
          $ref: '#/definitions/Error'
        examples:
          application/json:
            errors:
              name: ["Missing data for required field."]
    """
    data = request.get_json(silent=True) or {}
    try:
        m = mechanic_schema.load(data, session=db.session)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    pw = data.get("password")
    if pw:
        m.set_password(pw)

    db.session.add(m)
    db.session.commit()
    return mechanic_schema.jsonify(m), 201

# GET /mechanics  -> 200
@mechanics_bp.get("", strict_slashes=False)
def list_mechanics():
    """
    List mechanics
    ---
    tags: [Mechanics]
    summary: Get all mechanics
    produces:
      - application/json
    responses:
      200:
        description: A list of mechanics
        schema:
          type: array
          items:
            $ref: '#/definitions/Mechanic'
        examples:
          application/json: [{"mechanic_id":1,"name":"Sam Wrench","email":"sam@example.com"}]
    """
    allm = Mechanic.query.all()
    return jsonify(mechanics_schema.dump(allm)), 200


# GET /mechanics/<id>  -> 200
@mechanics_bp.get("/<int:id>")
def get_mechanic(id):
    """
    Get mechanic by id
    ---
    tags: [Mechanics]
    summary: Retrieve a mechanic
    parameters:
      - in: path
        name: id
        type: integer
        required: true
    responses:
      200:
        description: Mechanic
        schema:
          $ref: '#/definitions/Mechanic'
      404:
        description: Not found
        schema:
          $ref: '#/definitions/Error'
    """
    m = Mechanic.query.get_or_404(id)
    return jsonify(mechanic_schema.dump(m)), 200


# PUT /mechanics/<id>  -> 200
@mechanics_bp.route('/<int:id>', methods=['PUT'])
def update_mechanic(id):
    """
    Update Mechanic
    ---
    tags: [Mechanics]
    summary: Update an existing mechanic
    description: >
      Partially update a mechanic. Any provided fields will be updated.
      If **password** is provided it will be hashed and saved.
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: path
        name: id
        required: true
        type: integer
        description: Mechanic ID
      - in: body
        name: payload
        required: true
        schema:
          $ref: '#/definitions/MechanicUpdatePayload'
    responses:
      200:
        description: Updated mechanic
        schema:
          $ref: '#/definitions/Mechanic'
        examples:
          application/json:
            mechanic_id: 1
            name: "Sam Wrench"
            email: "sam@example.com"
            phone: "555-2222"
            salary: "55000.00"
            address: "456 Elm Rd"
      400:
        description: Validation error
        schema:
          $ref: '#/definitions/Error'
        examples:
          application/json:
            errors:
              email: ["Not a valid email address."]
      404:
        description: Mechanic not found
        schema:
          $ref: '#/definitions/Error'
        examples:
          application/json:
            error: "Not Found"
    """
    data = request.get_json(silent=True) or {}

    m = Mechanic.query.get_or_404(id)

    pw = data.get("password")
    if pw:
        m.set_password(pw)

    try:
        m = mechanic_schema.load(
            data, instance=m, session=db.session, partial=True
        )
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    db.session.commit()
    return mechanic_schema.jsonify(m), 200


# DELETE /mechanics/<id>  -> 204
@mechanics_bp.delete("/<int:id>")
def delete_mechanic(id):
    """
    Delete mechanic
    ---
    tags: [Mechanics]
    summary: Delete a mechanic
    parameters:
      - in: path
        name: id
        type: integer
        required: true
    responses:
      204:
        description: Deleted
      404:
        description: Not found
        schema:
          $ref: '#/definitions/Error'
    """
    m = Mechanic.query.get_or_404(id)
    db.session.delete(m)
    db.session.commit()
    return "", 204


# GET /mechanics/ranked  -> 200
@mechanics_bp.get("/ranked")
def get_ranked_mechanics():
    """
    Ranked mechanics
    ---
    tags: [Mechanics]
    summary: Mechanics ranked by assignment count
    responses:
      200:
        description: List of mechanics with assignment counts
        schema:
          type: array
          items:
            type: object
            properties:
              mechanic:
                $ref: '#/definitions/Mechanic'
              assignment_count:
                type: integer
    """
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
