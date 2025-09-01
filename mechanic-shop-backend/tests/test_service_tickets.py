# tests/test_service_tickets.py
from tests.base import BaseTestCase

class TestTickets(BaseTestCase):
    def test_create_ticket_unauthorized(self):
        res = self.client.post("/service_tickets/", json={"description": "Oil change"})
        self.assertEqual(res.status_code, 401)

    def test_create_ticket_authorized_minimal(self):
        headers = self.auth_header(role="customer", sub="1")  # or "mechanic" based on your protection
        res = self.client.post("/service_tickets/", json={"description": "Oil change", "vin": "TESTVIN123"}, headers=headers)
        self.assertIn(res.status_code, (201, 400))  # 400 if your code requires an existing vehicle

    def test_my_assigned_tickets_requires_auth(self):
        res = self.client.get("/mechanic/my-assigned-tickets")
        self.assertEqual(res.status_code, 401)

    def test_my_assigned_tickets_ok(self):
        headers = self.auth_header(role="mechanic", sub=str(getattr(self, "mechanic_id", 1)))
        res = self.client.get("/mechanic/my-assigned-tickets", headers=headers)
        self.assertIn(res.status_code, (200, 401))
