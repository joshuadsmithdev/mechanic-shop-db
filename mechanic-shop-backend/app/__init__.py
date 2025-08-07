from flask import Flask
from .config      import Config
from .extensions  import db, migrate, ma

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    # register blueprints
    from .blueprints.mechanics.routes     import mechanics_bp
    from .blueprints.service_tickets import tickets_bp
    from .blueprints.customers.routes import customers_bp
    from .blueprints.vehicles.routes import vehicles_bp
    app.register_blueprint(vehicles_bp,    url_prefix='/vehicles')

    app.register_blueprint(customers_bp)

    app.register_blueprint(mechanics_bp,   url_prefix='/mechanics')
    app.register_blueprint(tickets_bp,     url_prefix='/tickets')

    return app
