from django.core.management import call_command
from django.test import TestCase
from django.test import Client

class GeneralTest(TestCase):

    @classmethod
    def setUpClass(cls):
        # Note: we could use a fixture or decouple the
        # actual generator from the django command
        # (and/or both, actually) but this'll do for now.
        call_command('create_fake_users', 10)

    def test_index(self):
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_shorten(self):
        client = Client()
        response = client.post('/shorten', {
            'url': 'https://google.com/robots.txt'
        })
        self.assertEqual(response.status_code, 200)

    @classmethod
    def tearDownClass(cls):
        # Important! Don't remove this and leave the 
        # setUpClass method alone; this causes errors about
        # this class not having a 'cls_atomics' attribute.
        pass
