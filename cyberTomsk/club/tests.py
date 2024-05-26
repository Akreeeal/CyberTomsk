from django.test import TestCase



class TestCyberTomsk(TestCase):
    def test_home(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

