# mechanic_shop_backend/app/main.py
from flask import Flask, jsonify
from .config import Config
from .extensions import db, migrate, limiter, cache
from .demo import demo_bp
from .blueprints.customers.routes import customers_bp
# from flask_cors import CORS  # optional if calling from another origin
import os

app = Flask(__name__)
app.config.from_object(Config)

# Blueprints
app.register_blueprint(demo_bp)                              # /demo
app.register_blueprint(customers_bp, url_prefix="/api/customers")

# Extensions
db.init_app(app)
migrate.init_app(app, db)
limiter.init_app(app)
cache.init_app(app)

# ⬅️ CRITICAL: import models BEFORE create_all / migrations
from . import models  # noqa: F401

# Safety net: create any missing tables (e.g., if migrations didn’t run)
with app.app_context():
    try:
        db.create_all()
        # log what tables we see now
        insp = db.inspect(db.engine)
        app.logger.info("Startup tables: %s", sorted(insp.get_table_names()))
    except Exception as e:
        app.logger.exception("db.create_all() failed: %s", e)

# CORS if your UI is elsewhere
# CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.get("/diag")
def diag():
    try:
        uri = app.config.get("SQLALCHEMY_DATABASE_URI", "<missing>")
        insp = db.inspect(db.engine)
        return jsonify({
            "db_uri_sample": uri[:60] + ("..." if len(uri) > 60 else ""),
            "tables": sorted(insp.get_table_names())
        }), 200
    except Exception as e:
        app.logger.exception("diag failed")
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return "🔧 Mechanic Shop API is alive!"

@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.exception("Unhandled exception: %s", e)
    return jsonify({"error": "Internal Server Error"}), 500

if __name__ == "__main__":
    app.run(debug=True)
