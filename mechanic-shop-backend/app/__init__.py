from flask import Flask
from .config      import Config, os
from .extensions  import db, migrate, ma

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "fallback_dev_secret")

    # init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    # register blueprints
    from .blueprints.mechanics.routes     import mechanics_bp
    from .blueprints.service_tickets import tickets_bp
    from .blueprints.customers.routes import customers_bp
    from .blueprints.vehicles.routes import vehicles_bp
    from .blueprints.customers.ticket_routes import customer_ticket_bp
    from app.blueprints.mechanics.mechanic_ticket_routes import mechanic_ticket_bp



    app.register_blueprint(customers_bp)
    app.register_blueprint(mechanic_ticket_bp, url_prefix='/mechanic')
    app.register_blueprint(customer_ticket_bp, url_prefix='/customer')
    app.register_blueprint(vehicles_bp,    url_prefix='/vehicles')
    app.register_blueprint(mechanics_bp,   url_prefix='/mechanics')
    app.register_blueprint(tickets_bp,     url_prefix='/tickets')

    return app
