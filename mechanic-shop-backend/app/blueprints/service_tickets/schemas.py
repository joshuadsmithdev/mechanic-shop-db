from ...extensions import ma
from ...models import ServiceTicket

class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceTicket
        include_relationships = False  # 👈 Turn this OFF to stop auto-loading `vehicle`
        include_fk = True              # 👈 Required to allow `vin` input
        load_instance = True
        dump_only = ('ticket_id',)

    # Optional: define vin explicitly if needed
    # vin = ma.Str(required=True)
