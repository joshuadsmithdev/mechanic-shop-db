# app/blueprints/inventory/schemas.py
from marshmallow import fields, EXCLUDE
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.extensions import ma
from app.models import Inventory  # adjust import path/name if needed

class InventorySchema(ma.SQLAlchemyAutoSchema):
    # Expose `id` in API even if model uses `item_id`
    id = fields.Int(attribute="item_id", dump_only=True)

    # Accept test payload keys but map to your model fields:
    # - if your model uses `quantity`, map incoming `qty` -> `quantity`
    quantity = fields.Int(data_key="qty")

    # Make sku optional (tests send it, model may or may not store it)
    sku = fields.Str(required=False)
    price = fields.Decimal(required=False, as_string=True)

    class Meta:
        model = Inventory
        load_instance = True
        include_fk = True
        # Ignore unexpected keys instead of hard-failing
        # (helps if tests send `sku` and your model doesn't have it)
        unknown = EXCLUDE
