# mechanic_shop_backend/app/main.py
from . import create_app

# Gunicorn will import this "app"
app = create_app()

if __name__ == "__main__":
    # For local testing if you ever call this file directly
    app.run(debug=True)
