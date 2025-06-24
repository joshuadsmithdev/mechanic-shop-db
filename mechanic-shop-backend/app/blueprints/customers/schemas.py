from app.extensions import ma
from app.models import Customer

class CustomerSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Customer
        load_instance = True
        include_fk = True  # not strictly needed here but good habit

    customer_id = ma.auto_field(dump_only=True)
    first_name = ma.Str(required=True)
    last_name = ma.Str(required=True)
    phone = ma.Str()
    email = ma.Email()
    address = ma.Str()
