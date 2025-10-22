from flask import Flask, jsonify
from .config import Config
from .extensions import db, migrate, limiter, cache
from .demo import demo_bp
from .blueprints.customers.routes import customers_bp

# Optional CORS if your frontend is another origin (Netlify/GitHub Pages)
# from flask_cors import CORS

import os

app = Flask(__name__)
app.config.from_object(Config)

# If you want rate-limit headers, you can also:
# app.config.update(RATELIMIT_HEADERS_ENABLED=True)

# Blueprints
app.register_blueprint(demo_bp)                              # GET /demo
app.register_blueprint(customers_bp, url_prefix="/api/customers")

# Extensions
db.init_app(app)
migrate.init_app(app, db)
limiter.init_app(app)
cache.init_app(app)

# Ensure models are imported so Flask-Migrate sees them
from . import models  # noqa: E402,F401  (keep after db.init_app)

# ---------- TEMP: safety net to create tables if migrations didn’t ----------
# This is safe: it only creates tables that don't exist yet.
with app.app_context():
    try:
        db.create_all()
    except Exception as e:
        app.logger.exception("db.create_all() failed: %s", e)
# ---------------------------------------------------------------------------

# ---------- TEMP: diagnostics you can hit in the browser ----------
@app.get("/diag")
def diag():
    """Quick diagnostics to confirm DB + tables."""
    try:
        uri = app.config.get("SQLALCHEMY_DATABASE_URI", "<missing>")
        # Reflect available tables
        insp = db.inspect(db.engine)
        tables = sorted(insp.get_table_names())
        return jsonify({
            "db_uri_sample": uri[:60] + ("..." if len(uri) > 60 else ""),
            "tables": tables
        }), 200
    except Exception as e:
        app.logger.exception("diag failed")
        return jsonify({"error": str(e)}), 500
# ------------------------------------------------------------------

# Optional CORS (uncomment if calling API from a different domain)
# CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route("/")
def home():
    return "🔧 Mechanic Shop API is alive!"

# Helpful error logging (keeps stacktraces in Render logs)
@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.exception("Unhandled exception: %s", e)
    return jsonify({"error": "Internal Server Error"}), 500

if __name__ == "__main__":
    app.run(debug=True)
