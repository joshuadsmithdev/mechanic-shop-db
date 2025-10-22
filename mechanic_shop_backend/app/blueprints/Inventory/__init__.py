from flask import Blueprint

inventory_bp = Blueprint("inventory", __name__)

from . import routes  # ensure routes are loaded
