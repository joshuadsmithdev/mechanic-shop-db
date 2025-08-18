from marshmallow import Schema, fields

class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)

from app.extensions import ma
from app.models import Customer

class CustomerSchema(ma.SQLAlchemyAutoSchema):
    id = fields.Int(attribute="customer_id", dump_only=True)  # map model's customer_id to id in API
     # explicitly include fields that are not picked up by default
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    address = fields.Str(required=True)
    phone = fields.Str(required=True)
    password = fields.Str(load_only=True, required=True)
    class Meta:
        model = Customer
        load_instance = True
        include_fk = True  # not strictly needed here but good habit
        exclude = ("password_hash",)  # Exclude password hash from output
