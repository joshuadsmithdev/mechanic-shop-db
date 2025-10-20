# app/models/__init__.py
from .customer import Customer
from .vehicle import Vehicle
from .mechanic import Mechanic
from .service_ticket import ServiceTicket
from .service_assignment import ServiceAssignment
from .inventory import Inventory

__all__ = [
    "Customer",
    "Vehicle",
    "Mechanic",
    "ServiceTicket",
    "ServiceAssignment",
    "Inventory",
]
