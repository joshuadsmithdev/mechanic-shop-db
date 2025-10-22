# mechanic_shop_backend/app/main.py
from flask import Flask, jsonify
from .config import Config
from .extensions import db, migrate, limiter, cache

# Blueprints
from .demo import demo_bp
from .blueprints.customers.routes import customers_bp
# (add others later as needed)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # --- Init extensions ---
    db.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)   # works with Flask-Limiter 3.x/4.x without kwargs
    cache.init_app(app)

    # --- Register blueprints ---
    app.register_blueprint(demo_bp)  # serves /demo
    app.register_blueprint(customers_bp, url_prefix="/api/customers")

    # --- Ensure tables exist at startup (Postgres-safe) ---
    # Important: import models BEFORE create_all so metadata is populated.
    with app.app_context():
        from . import models  # noqa: F401 - populates db.metadata
        try:
            db.create_all()  # creates missing tables (no-op if they already exist)
            app.logger.info("DB create_all() completed.")
        except Exception:
            app.logger.exception("DB create_all() failed")

    # --- Simple health/diag routes ---
    @app.get("/")
    def home():
        return "🔧 Mechanic Shop API is alive!"

    @app.get("/diag")
    def diag():
        # Show DB URI start (not full) and current tables visible to SQLAlchemy
        try:
            uri = app.config.get("SQLALCHEMY_DATABASE_URI", "")
            sample = f"{uri[:60]}..." if uri else "unset"
            # Reflect to see server-side tables
            from sqlalchemy import inspect
            insp = inspect(db.engine)
            tables = insp.get_table_names()
            return jsonify({"db_uri_sample": sample, "tables": tables}), 200
        except Exception as e:
            app.logger.exception("diag failed")
            return jsonify({"error": str(e)}), 500

    return app

# Gunicorn entrypoint expects a module-level `app`
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
