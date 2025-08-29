from rest_framework.test import APITestCase
from django.urls import reverse


class HealthTests(APITestCase):
    def test_health(self):
        url = reverse('Health')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"message": "Server is up!"})


class AuthAndNotesTests(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')

    def test_register_login_create_note_flow(self):
        # Register
        res = self.client.post(self.register_url, {"username": "u1", "email": "u1@example.com", "password": "password123"})
        self.assertEqual(res.status_code, 201)
        # Login
        res = self.client.post(self.login_url, {"username": "u1", "password": "password123"})
        self.assertEqual(res.status_code, 200)
        # Create note
        res = self.client.post("/api/notes/", {"title": "First", "content": "Hello"})
        self.assertEqual(res.status_code, 201)
        note_id = res.data["id"]
        # List notes
        res = self.client.get("/api/notes/")
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(res.data) >= 1)
        # Retrieve note
        res = self.client.get(f"/api/notes/{note_id}/")
        self.assertEqual(res.status_code, 200)
        # Update note
        res = self.client.patch(f"/api/notes/{note_id}/", {"title": "Updated"})
        self.assertEqual(res.status_code, 200)
        # Delete note
        res = self.client.delete(f"/api/notes/{note_id}/")
        self.assertEqual(res.status_code, 204)
        # Logout
        res = self.client.post(self.logout_url)
        self.assertEqual(res.status_code, 200)
