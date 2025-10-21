from flask_sqlalchemy import SQLAlchemy
from flask_migrate    import Migrate
from flask_marshmallow import Marshmallow
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache

limiter = Limiter(
  key_func=get_remote_address,
  storage_uri="memory://",   # ✅ in-memory store (perfect for Render)
    default_limits=[]          # ✅ optional; disables global default rate limits
)
cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})

db     = SQLAlchemy()
migrate = Migrate()
ma     = Marshmallow()
