# mechanic_shop_backend/app/main.py
from flask import Flask
from .config import Config
from .extensions import db, migrate, limiter, cache
from .demo import demo_bp
from .blueprints.customers.routes import customers_bp

app = Flask(__name__)
app.config.from_object(Config)

# Blueprints
app.register_blueprint(demo_bp)                              # GET /demo
app.register_blueprint(customers_bp, url_prefix="/api/customers")

# Extensions
db.init_app(app)
migrate.init_app(app, db)
limiter.init_app(app)    # <-- no kwargs here
cache.init_app(app)
from . import models
@app.route("/")
def home():
    return "🔧 Mechanic Shop API is alive!"

if __name__ == "__main__":
    app.run(debug=True)
