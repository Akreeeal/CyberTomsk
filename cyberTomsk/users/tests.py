from django.test import TestCase
from django.utils import timezone

from .forms import ProfileUserForm
from .models import User
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm

class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass',
            date_birth=timezone.make_aware(timezone.datetime(2000, 1, 1))  # timezone-aware дата
        )

    def test_user_str(self):
        self.assertEqual(str(self.user), 'testuser')

    def test_user_photo_blank(self):
        self.assertIsNone(self.user.photo.name)  # Проверяем, что имя файла фотографии None

    def test_user_date_birth(self):
        self.assertEqual(self.user.date_birth.strftime('%Y-%m-%d'), '2000-01-01')
#
#
class LoginUsersTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')

    def test_login_view_status_code(self):
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)

    def test_login_view_template_used(self):
        response = self.client.get(reverse('users:login'))
        self.assertTemplateUsed(response, 'users/login.html')

    def test_login_view_form(self):
        response = self.client.get(reverse('users:login'))
        self.assertIsInstance(response.context['form'], AuthenticationForm)

    def test_login_view_success(self):
        response = self.client.post(reverse('users:login'), {'username': 'testuser', 'password': 'testpass'})
        self.assertRedirects(response, reverse('club:home'))
#
class ProfileUserTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass',
                                                         email='testuser@example.com')
        self.client.login(username='testuser', password='testpass')

    def test_profile_view_status_code(self):
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 200)

    def test_profile_view_template_used(self):
        response = self.client.get(reverse('users:profile'))
        self.assertTemplateUsed(response, 'users/profile.html')

    def test_profile_view_form(self):
        response = self.client.get(reverse('users:profile'))
        self.assertIsInstance(response.context['form'], ProfileUserForm)

class UserIntegrationTest(TestCase):
    def test_user_registration_and_login(self):
        # Test user registration
        registration_url = reverse('users:register')
        registration_data = {
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'email': 'testuser@example.com',
        }
        response = self.client.post(registration_url, registration_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(get_user_model().objects.filter(username='testuser').exists())

        # Test user login
        login_url = reverse('users:login')
        login_data = {
            'username': 'testuser',
            'password': 'testpassword',
        }
        response = self.client.post(login_url, login_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.wsgi_request.user.is_authenticated)