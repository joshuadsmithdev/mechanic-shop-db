# app/utils/token.py
from __future__ import annotations

import os
from functools import wraps
from datetime import datetime as dt, timedelta as td
from typing import Optional, Callable, Any

from flask import request, jsonify, current_app
from jose import jwt, JWTError

ALGO = "HS256"

def _secret_candidates() -> list[str]:
    # Try Flask config, then env var, then a dev fallback
    cand = []
    if current_app and current_app.config.get("SECRET_KEY"):
        cand.append(current_app.config["SECRET_KEY"])
    if os.getenv("SECRET_KEY"):
        cand.append(os.getenv("SECRET_KEY"))
    cand.append("fallback_dev_secret")
    # de-dup while preserving order
    seen = set()
    out = []
    for k in cand:
        if k and k not in seen:
            out.append(k)
            seen.add(k)
    return out

def encode_token(sub: str | int, role: Optional[str] = None, expires_in: int = 60 * 60 * 8) -> str:
    now = dt.utcnow()
    payload = {
        "sub": str(sub),
        "iat": int(now.timestamp()),
        "exp": int((now + td(seconds=expires_in)).timestamp()),
    }
    if role:
        payload["role"] = role
    return jwt.encode(payload, _secret_candidates()[0], algorithm=ALGO)

def decode_jwt(token: str) -> dict:
    last_err = None
    for key in _secret_candidates():
        try:
            return jwt.decode(token, key, algorithms=[ALGO])
        except JWTError as e:
            last_err = e
            continue
    # if nothing worked, raise the last error
    raise last_err or JWTError("Invalid token")

def _extract_token_from_headers() -> Optional[str]:
    # accept multiple common header spellings
    headers = request.headers or {}
    candidates = [
        headers.get("Authorization"),
        headers.get("authorization"),
        headers.get("X-Access-Token"),
        headers.get("x-access-token"),
        headers.get("X-ACCESS-TOKEN"),
        request.environ.get("HTTP_AUTHORIZATION"),
        request.environ.get("Authorization"),
    ]
    for raw in candidates:
        if not raw:
            continue
        h = raw.strip()
        # Allow "Bearer xyz" or just "xyz"
        if h.lower().startswith("bearer "):
            h = h[7:].strip()
        elif h.lower().startswith("bearer"):
            h = h[6:].strip()
        if h:
            return h
    return None

def token_required(*roles: str) -> Callable[..., Any]:
    def decorator(fn: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            token = _extract_token_from_headers()
            if not token:
                return jsonify({"error": "Missing or invalid Authorization header"}), 401

            try:
                payload = decode_jwt(token)
            except JWTError:
                return jsonify({"error": "Invalid token"}), 401

            role = payload.get("role")
            if roles and role not in roles:
                return jsonify({"error": "Forbidden"}), 403

            # pass-through convenience args if caller wants them
            code_vars = getattr(fn, "__code__", None)
            varnames = getattr(code_vars, "co_varnames", ()) if code_vars else ()
            if "current_user_id" in varnames:
                kwargs["current_user_id"] = payload.get("sub")
            if "current_role" in varnames:
                kwargs["current_role"] = role

            return fn(*args, **kwargs)
        return wrapper
    return decorator
