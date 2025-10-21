
# Customers Demo UI (Drop-in)

This package adds a simple **/demo** page that lets users interact with your existing
`/api/customers` endpoints (list, create, get, update, delete) using HTMX + fetch.

## Files to copy
- `app/demo.py`
- `app/templates/demo.html`
- `app/static/demo_customers.css`
- `app/static/demo_customers.js`

## Register the blueprint
In your app factory (after you create `app`):
```python
from app.demo import demo_bp
app.register_blueprint(demo_bp)  # serves GET /demo
```

## Notes
- No changes to your existing customers blueprint are required.
- If you use rate limiting, fast repeated clicks may hit limits (expected).
- Link it from your landing page: `<a href="/demo" target="_blank">Live Demo</a>`.
