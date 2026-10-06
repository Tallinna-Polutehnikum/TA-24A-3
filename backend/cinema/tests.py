from django.test import SimpleTestCase
from django.urls import reverse


class HealthViewTests(SimpleTestCase):
    def test_health_endpoint_returns_app_status(self):
        response = self.client.get(reverse('cinema:health'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'app': 'cinema',
            'status': 'ok',
        })
