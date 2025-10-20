# tests/base.py
import os
import unittest
from app import create_app, db
from app.models import Customer, Vehicle, Mechanic
from werkzeug.security import generate_password_hash
from app.utils.token import encode_token

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        # Ensure a deterministic secret for encode/decode during tests
        os.environ.setdefault("SECRET_KEY", "test-secret-key")

        self.app = create_app({
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite://",
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            # Make sure Flask config also sees the same secret
            "SECRET_KEY": os.environ["SECRET_KEY"],
        })
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

            # Seed a default customer used by auth tests
            if not Customer.query.filter_by(email="sam@example.com").first():
                c = Customer(
                    customer_id=1,
                    email="sam@example.com",
                    address="",
                    phone="555-1111",
                )
                # Your model uses password_hash; set it explicitly
                c.password_hash = generate_password_hash("secret123")
                db.session.add(c)

            # Seed a mechanic for the mechanic-auth tests (optional)
            if not Mechanic.query.filter_by(email="mech@example.com").first():
                m = Mechanic(
                    mechanic_id=1,
                    name="Alex Wrench",
                    email="mech@example.com",
                    phone="555-2222",
                    salary=0,
                )
                if hasattr(m, "set_password"):
                    m.set_password("secret123")
                else:
                    m.password_hash = generate_password_hash("secret123")
                db.session.add(m)

            # OPTIONAL: seed a vehicle so create_ticket can return 201
            # Comment these two lines if you want the test to get 400 instead.
            if not Vehicle.query.filter_by(vin="TESTVIN123").first():
                db.session.add(Vehicle(vin="TESTVIN123", customer_id=1))

            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def auth_header(self, role="customer", sub="1"):
        """
        Generate a JWT inside the app context so encode_token and decode_jwt
        use the exact same SECRET_KEY source.
        """
        with self.app.app_context():
            token = encode_token(sub=sub, role=role)
        return {"Authorization": f"Bearer {token}"}

    # Handy if a specific test wants to ensure a VIN exists
    def ensure_vehicle(self, vin="TESTVIN123", customer_id=1):
        with self.app.app_context():
            if not Vehicle.query.filter_by(vin=vin).first():
                db.session.add(Vehicle(vin=vin, customer_id=customer_id))
                db.session.commit()
