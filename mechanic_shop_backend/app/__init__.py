# app/__init__.py
from flask import Flask, jsonify, Response
import os
from ..config import Config
from .extensions import db, migrate, ma
from flask_swagger_ui import get_swaggerui_blueprint

def create_app(config_overrides=None):
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.config.from_object(Config)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "fallback_dev_secret")

    if config_overrides:
        app.config.update(config_overrides)

    # init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    # import models so tables are registered
    from . import models  # noqa

    # Swagger UI
    SWAGGER_URL = "/docs"
    API_URL = "/swagger.json"
    swaggerui_bp = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={"app_name": "Mechanic Shop API"})
    app.register_blueprint(swaggerui_bp, url_prefix=SWAGGER_URL)

    from .swagger import swagger_spec
    @app.route("/swagger.json")
    def swagger_json():
        return jsonify(swagger_spec)

    # --- Blueprints (NOTE the /api prefixes) ---
    from .blueprints.customers.routes import customers_bp
    from .blueprints.inventory.routes import inventory_bp
    from .blueprints.mechanics.routes import mechanics_bp
    from .blueprints.service_tickets.routes import tickets_bp
    from .blueprints.vehicles.routes import vehicles_bp
    from .blueprints.customers.ticket_routes import customer_ticket_bp
    from .blueprints.mechanics.mechanic_ticket_routes import mechanic_ticket_bp
    from .blueprints.auth.routes import auth_bp

    app.register_blueprint(customers_bp,       url_prefix="/api/customers")
    app.register_blueprint(inventory_bp,       url_prefix="/api/inventory")
    app.register_blueprint(mechanics_bp,       url_prefix="/api/mechanics")
    app.register_blueprint(tickets_bp,         url_prefix="/api/service_tickets")
    app.register_blueprint(vehicles_bp,        url_prefix="/api/vehicles")
    app.register_blueprint(customer_ticket_bp, url_prefix="/api/customer")
    app.register_blueprint(mechanic_ticket_bp, url_prefix="/api/mechanic")
    app.register_blueprint(auth_bp)
    @app.route("/diag/routes")
    def diag_routes():
        out = []
        for r in app.url_map.iter_rules():
            out.append({
                "rule": r.rule,
                "methods": sorted(m for m in r.methods if m in {"GET","POST","PUT","DELETE","PATCH"})
            })
        return jsonify(sorted(out, key=lambda x: x["rule"]))

    @app.errorhandler(404)
    def handle_404(e):
        html = (
            "<!doctype html><html lang='en'><head><meta charset='utf-8'><title>Not Found</title></head>"
            "<body><h1>Not Found</h1><p>The requested URL was not found on the server.</p></body></html>"
        )
        return Response(html, status=404, headers={"Content-Type": "text/html"})

    @app.errorhandler(405)
    def handle_405(e):
        return Response("Method Not Allowed", status=405, headers={"Content-Type": "text/html"})

    return app
