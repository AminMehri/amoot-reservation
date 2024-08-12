from django.test import TestCase, Client
from django.urls import reverse
from Account.models import Account, User

class RegisterViewTest(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.url = reverse('register')

    def test_register_user_success(self):
        response = self.client.post(self.url, {
            'username': 'testuser',
            'password': 'testpass123',
            'email': 'test.test@test.test'
        })

        # Check status code
        self.assertEqual(response.status_code, 200)

        # Check message
        self.assertEqual(response.json().get('message'), 'user testuser created successfully')

        # Check user created
        self.assertTrue(Account.objects.filter(user__username='testuser').exists())

    def test_register_user_invalid_email(self):
        response = self.client.post(self.url, {
            'username': 'testuser',
            'password': 'testpass123',
            'email': 'invalidemail'
        })

        # Check status code
        self.assertEqual(response.status_code, 400)

        # Check message
        self.assertEqual(response.json().get('message'), 'invalid data')

        # Check user not created
        self.assertFalse(Account.objects.filter(user__username='testuser').exists())

    def test_register_user_existing_username(self):
        User.objects.create_user(username='testuser', password='testpass123', email='test.test@test.test')
        response = self.client.post(self.url, {
            'username': 'testuser',
            'password': 'testpass123',
            'email': 'test2.test2@test2.test2'
        })

        # Check status code
        self.assertEqual(response.status_code, 406)

        # Check message
        self.assertEqual(response.json().get('message'), 'username is already exist')

        # Check user not created
        self.assertFalse(Account.objects.filter(user__username='testuser').exists())