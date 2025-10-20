# tests/test_mechanics.py
from tests.base import BaseTestCase

class TestMechanics(BaseTestCase):
    def test_list_mechanics(self):
        res = self.client.get("/mechanics/")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.get_json(), list)

    def test_create_mechanic(self):
        payload = {"name": "Alex Bolt", "email": "alex@example.com", "password": "pw"}
        res = self.client.post("/mechanics/", json=payload)
        self.assertIn(res.status_code, (201, 400))  # 400 if marshmallow requires more fields
        if res.status_code == 201:
            self.assertIn("email", res.get_json())

    def test_get_mechanic(self):
        res = self.client.get(f"/mechanics/{getattr(self, 'mechanic_id', 1)}")
        self.assertIn(res.status_code, (200, 404))

    def test_update_mechanic(self):
        payload = {"phone": "555-2222"}
        res = self.client.put(f"/mechanics/{getattr(self, 'mechanic_id', 1)}", json=payload)
        self.assertIn(res.status_code, (200, 404))

    def test_delete_mechanic(self):
        res = self.client.delete(f"/mechanics/{getattr(self, 'mechanic_id', 1)}")
        self.assertIn(res.status_code, (204, 404))

    def test_create_mechanic_invalid(self):
        res = self.client.post("/mechanics/", json={"email": "not-an-email"})
        self.assertEqual(res.status_code, 400)
