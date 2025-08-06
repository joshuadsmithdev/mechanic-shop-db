from jose import jwt, JWTError
from datetime import datetime, timedelta

SECRET_KEY = "your_secret_key_here"  # Replace with a strong key, or use `app.config`
ALGORITHM = "HS256"
EXPIRE_MINUTES = 60  # Token expires in 1 hour

def encode_token(customer_id):
    payload = {
        "sub": customer_id,
        "exp": datetime.utcnow() + timedelta(minutes=EXPIRE_MINUTES)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]
    except JWTError:
        return None
def token_required(f):
    """
    Decorator to require a valid token for accessing a route.
    """
    from functools import wraps
    from flask import request, jsonify

    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Authorization header missing or invalid"}), 401

        parts = auth_header.split()
        if len(parts) != 2:
            return jsonify({"error": "Invalid authorization header format"}), 401

        token = parts[1]

        customer_id = decode_token(token)
        if not customer_id:
            return jsonify({"error": "Invalid token"}), 401

        return f(customer_id, *args, **kwargs)

    return decorated_function
