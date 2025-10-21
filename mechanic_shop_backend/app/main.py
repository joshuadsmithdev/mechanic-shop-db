from flask import Flask
from ..config import Config
from .extensions import db, migrate, limiter, cache
from .demo import demo_bp

app = Flask(__name__)
app.config.from_object(Config)

app.register_blueprint(demo_bp)  # Serves GET /demo


# Initialize extensions
db.init_app(app)
migrate.init_app(app, db)
limiter.init_app(app)
cache.init_app(app)

@app.route("/")
def home():
    return "🔧 Mechanic Shop API is alive!"

if __name__ == "__main__":
    app.run(debug=True)
