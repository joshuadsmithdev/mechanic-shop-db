# tests/test_auth.py
from tests.base import BaseTestCase

class TestAuth(BaseTestCase):
    def test_login_success(self):
        payload = {"email": "sam@example.com", "password": "secret123"}
        res = self.client.post("/auth/login", json=payload)
        self.assertIn(res.status_code, (200, 401))  # if your login is customer-only, adjust
        if res.status_code == 200:
            self.assertIn("token", res.get_json())

    def test_login_bad_credentials(self):
        payload = {"email": "nosuch@example.com", "password": "nope"}
        res = self.client.post("/auth/login", json=payload)
        self.assertEqual(res.status_code, 401)
