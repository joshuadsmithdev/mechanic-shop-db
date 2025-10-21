
from flask import Blueprint, render_template

demo_bp = Blueprint("demo", __name__)

@demo_bp.get("/demo", strict_slashes=False)
def demo_page():
    # Renders the HTMX UI wired to /api/customers endpoints
    return render_template("demo.html")
