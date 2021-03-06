from core.models import User
from django.core.management import call_command
from django.test import Client, TestCase


class CreateFakeUsersTest(TestCase):
    def test_command(self):
        call_command('create_fake_users', 10)
        user_count = User.objects.count()
        self.assertEqual(user_count, 10)


class GeneralTest(TestCase):
    """
    A really minimal set of smoketests to make sure
    things at least look OK on the surface.
    """

    @classmethod
    def setUpClass(cls):
        # Note: we could use a fixture or decouple the
        # actual generator from the django command
        # (and/or both, actually) but this'll do for now.
        call_command('create_fake_users', 10)

    def test_index(self):
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 302)

    def test_shorten(self):
        TEST_URL = 'https://google.com/robots.txt'
        client = Client()
        response = client.post('/shorten', {
            'url': TEST_URL
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(TEST_URL in response.content.decode('utf-8'))

    @classmethod
    def tearDownClass(cls):
        # Important! Don't remove this and leave the
        # setUpClass method alone; this causes errors about
        # this class not having a 'cls_atomics' attribute.
        pass
