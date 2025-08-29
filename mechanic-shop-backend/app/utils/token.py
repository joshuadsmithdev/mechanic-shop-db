# app/utils/token.py
from jose import jwt, JWTError
from datetime import datetime, timedelta, UTC
from functools import wraps
from flask import current_app, request, jsonify

# -------------------------------------------------------------------
# Config / Defaults
# -------------------------------------------------------------------
ALGORITHM = "HS256"
EXPIRE_MINUTES = 60  # Token expires in 1 hour

# NOTE: this is a fallback. In production you should set app.config["SECRET_KEY"]
# and not rely on this value.
SECRET_KEY = "secret123"  # ← override via app.config["SECRET_KEY"]


def _get_secret_key() -> str:
    """Return the secret key from Flask config, falling back to module constant."""
    try:
        key = current_app.config.get("SECRET_KEY")
    except RuntimeError:
        # current_app not available (e.g., during import or CLI)
        key = None
    return key or SECRET_KEY


# -------------------------------------------------------------------
# Token Encode / Decode
# -------------------------------------------------------------------
def encode_token(user_id, role: str = "customer", expires_minutes: int = EXPIRE_MINUTES) -> str:
    """
    Create a signed JWT for the given user and role.
    Compatible with existing usages that only expect 'sub'.
    """
    payload = {
        "sub": str(user_id),
        "role": role,
        "iat": datetime.now(UTC),
        "exp": datetime.now(UTC) + timedelta(minutes=expires_minutes),
    }
    key = _get_secret_key()
    print(f"[encode_token] Using key: {key!r}, payload: {payload}")
    return jwt.encode(payload, key, algorithm=ALGORITHM)


def decode_jwt(token: str):
    """
    Decode a JWT and return the full payload dict, or None on failure.
    """
    key = _get_secret_key()
    print(f"[decode_jwt] Decoding with key: {key!r}, token: {token}")
    try:
        payload = jwt.decode(token, key, algorithms=[ALGORITHM])
        print(f"[decode_jwt] Decoded payload: {payload}")
        return payload
    except JWTError as e:
        print(f"[decode_jwt] JWT decode error: {type(e)} - {e}")
        return None


# Back-compat helper: return just the subject (customer_id/user_id) or None
def decode_token(token: str):
    """
    Legacy helper kept for backward compatibility with existing code that expects `sub`.
    Returns the subject (string user id) or None.
    """
    payload = decode_jwt(token)
    return payload.get("sub") if payload else None


# -------------------------------------------------------------------
# Decorator
# -------------------------------------------------------------------
def _wrap_with_auth(view_func, allowed_roles: tuple[str, ...]):
    """
    Inner wrapper that enforces a valid Bearer token and optional role checks.
    Injects the user id (sub) as the first positional argument to the view.
    """
    @wraps(view_func)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        print(f"[token_required] Authorization header: {auth_header!r}")

        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Authorization header missing or invalid"}), 401

        token = auth_header.split(" ", 1)[1]
        print(f"[token_required] Extracted token: {token!r}")

        payload = decode_jwt(token)
        if not payload:
            return jsonify({"error": "Invalid or expired token"}), 401

        user_id = payload.get("sub")
        role = payload.get("role")
        if not user_id:
            return jsonify({"error": "Invalid token payload"}), 401

        if allowed_roles and role not in allowed_roles:
            print(f"[token_required] Role {role!r} not in allowed {allowed_roles}")
            return jsonify({"error": "Forbidden"}), 403

        print(f"[token_required] OK: sub={user_id!r}, role={role!r}")
        # Inject user_id as the first positional argument (back-compat with your routes)
        return view_func(user_id, *args, **kwargs)

    return decorated_function


def token_required(*roles_or_fn):
    """
    Usage:
      @token_required                # any valid token
      @token_required()              # any valid token
      @token_required("mechanic")    # only mechanic role
      @token_required("customer","admin")

    The wrapped view will receive the decoded subject (user id) as the first
    positional argument.

    This decorator supports both direct and parameterized usage.
    """
    # Direct usage: @token_required
    if roles_or_fn and callable(roles_or_fn[0]):
        func = roles_or_fn[0]
        return _wrap_with_auth(func, ())
    # Parameterized usage: @token_required("role1", "role2", ...)
    else:
        allowed = tuple(roles_or_fn)
        def decorator(func):
            return _wrap_with_auth(func, allowed)
        return decorator
