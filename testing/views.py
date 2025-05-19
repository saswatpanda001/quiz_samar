from django.test import TestCase
from django.urls import reverse

class ViewTests(TestCase):
    def test_landing_page(self):
        response = self.client.get(reverse("hub:landing"))
        self.assertEqual(response.status_code, 200)  # Should return HTTP 200 OK
