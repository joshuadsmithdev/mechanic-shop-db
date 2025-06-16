from ...extensions import ma
from ...models     import ServiceTicket

class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceTicket
        include_relationships = True
        load_instance = True
        load_only    = ('vehicle',)
        dump_only    = ('ticket_id',)
