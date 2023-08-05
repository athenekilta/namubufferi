from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse
from django.core import mail
from accounts.models import CustomUser, PassPhrase, TermsOfService, PrivacyPolicy
from django.conf import settings

class TestLogin(TestCase):
    def test_login_required(self):
        url = reverse('ledger:buy')
        response = self.client.get(url)
        self.assertRedirects(response, '/login/')

    def test_login_view_contains_links_to_signup_and_lost_password(self):
        url = reverse('accounts:login')
        response = self.client.get(url)
        self.assertContains(response, 'href="/signup/"')
        self.assertContains(response, 'href="/password_reset/"')

class TestLogout(TestCase):
    def test_logout(self):
        user = create_test_user_in_db()
        self.client.login(username='testuser', password='testpassword')
        
        url = reverse('ledger:buy')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertFalse(response.wsgi_request.user.is_anonymous)

        url = reverse('accounts:logout')
        response = self.client.get(url)
        self.assertRedirects(response, '/login/')

        self.assertTrue(response.wsgi_request.user.is_anonymous)

        url = reverse('ledger:buy')
        response = self.client.get(url)
        self.assertRedirects(response, '/login/')

class TestSignup(TestCase):
    def test_signup_form_submission(self):
        # Check that there is no user with the email address we will use for testing
        self.assertFalse(CustomUser.objects.filter(email='test@example.com').exists())

        # Visit the signup page
        url = reverse('accounts:signup')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Submit the signup form with incomplete data
        data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'accept_terms': True,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)

        # Check that a user was not activated
        self.assertFalse(CustomUser.objects.filter(email='test@example.com', is_active=True).exists())

        # Check that an email was sent
        self.assertEqual(len(mail.outbox), 1)

        # Check the contents of the email
        email = mail.outbox[0]
        self.assertEqual(email.to, ['test@example.com'])
        self.assertEqual(email.subject, f'{settings.EMAIL_SUBJECT_PREFIX} Activate your Namubufferi account')
        self.assertIn('Hi testuser,', email.body)
        self.assertIn('http://', email.body)

        # Click on the link in the email
        activation_url = email.body.split('http://')[1].split('\n')[0]
        response = self.client.get(f'http://{activation_url}')
        self.assertEqual(response.status_code, 302)

        # Check that the user was activated
        self.assertTrue(CustomUser.objects.filter(email='test@example.com', is_active=True).exists())

        # Check that the user can log in
        self.client.login(username='testuser', password='testpassword')
        url = reverse('ledger:buy')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_signup_with_already_existing_email(self):
        user = create_test_user_in_db()
        url = reverse('accounts:signup')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Submit the signup form with incomplete data
        data = {
            'email': user.email,
            'username': 'testuser1',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'accept_terms': True,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertWarnsMessage(response.wsgi_request, 'A user with that email already exists.')
        
    def test_signup_with_already_existing_username(self):
        user = create_test_user_in_db()
        url = reverse('accounts:signup')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Submit the signup form with incomplete data
        data = {
            'email': 'test1@example.com',
            'username': user.username,
            'password1': 'testpassword',
            'password2': 'testpassword',
            'accept_terms': True,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertWarnsMessage(response.wsgi_request, 'A user with that username already exists.')

    def test_signup_with_correct_passphrase(self):
        passphrase = PassPhrase.load()
        passphrase.passphrase = 'testpassphrase'
        passphrase.save()
        url = reverse('accounts:signup')
        response = self.client.get(url)

        # Submit the signup form with incomplete data
        data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'passphrase': 'testpassphrase',
            'accept_terms': True,
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('accounts:login'))

    def test_signup_with_incorrect_passphrase(self):
        passphrase = PassPhrase.load()
        passphrase.passphrase = 'testpassphrase'
        passphrase.save()
        url = reverse('accounts:signup')
        response = self.client.get(url)

        # Submit the signup form with incomplete data
        data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'passphrase': 'incorrectpassphrase',
            'accept_terms': True,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertWarnsMessage(response.wsgi_request, 'Incorrect passphrase.')
        
class TestPasswordReset(TestCase):
    def test_password_reset_form_submission(self):
        user = create_test_user_in_db()
        url = reverse('accounts:password_reset')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Submit the password reset form with incomplete data
        data = {
            'email': user.email,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)

        # Check that an email was sent
        self.assertEqual(len(mail.outbox), 1)

        # Check the contents of the email
        email = mail.outbox[0]
        self.assertEqual(email.to, [user.email])
        self.assertEqual(email.subject, f'{settings.EMAIL_SUBJECT_PREFIX} Password reset on Namubufferi')
        self.assertIn('Hi testuser,', email.body)
        self.assertIn('http://', email.body)

        # Click on the link in the email
        reset_url = email.body.split('http://')[1].split('\n')[0]
        response = self.client.get(f'http://{reset_url}')
        self.assertEqual(response.status_code, 302)

        # Check that the reset URL is valid
        self.assertIn('/reset/', response.url)

        # Follow the link to the set-password page
        response = self.client.get(response.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('/set-password/', response.request.get('PATH_INFO'))

        # Change the password
        data = {
            'new_password1': 'newpassword123',
            'new_password2': 'newpassword123',
        }
        response = self.client.post(response.request.get('PATH_INFO'), data)
        self.assertRedirects(response, '/password_reset_complete/')

        # Check that the user can log in with the new password
        url = reverse('accounts:login')
        response = self.client.get(url)
        data = {
            'username': user.username,
            'password': 'newpassword123',
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, '/')
        self.assertTrue(self.client.login(username='testuser', password='newpassword123'))

        # check that the user can access the buy page
        current_url = reverse('ledger:buy')
        response = self.client.get(current_url)
        self.assertEqual(response.status_code, 200)

class TestProfileChangePassword(TestCase):
    def test_change_password(self):
        user = create_test_user_in_db()
        self.client.login(username='testuser', password='testpassword')

        url = reverse('accounts:profile_change_password')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Submit the change password form with incomplete data
        data = {
            'old_password': 'testpassword',
            'new_password1': 'newpassword123',
            'new_password2': 'newpassword123',
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, '/')

        # Check that the user can log in with the new password
        url = reverse('accounts:login')
        response = self.client.get(url)
        data = {
            'username': user.username,
            'password': 'newpassword123',
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, '/')

        self.assertTrue(self.client.login(username='testuser', password='newpassword123'))
    
class TestProfileDelete(TestCase):
    def test_delete_profile(self):
        user = create_test_user_in_db()
        self.client.login(username='testuser', password='testpassword')

        url = reverse('accounts:profile_delete_account')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Submit the delete profile form with incomplete data
        data = {
            'password': 'testpassword',
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, '/login/')

        # Check that the user can't log in with the old password
        url = reverse('accounts:login')
        response = self.client.get(url)
        data = {
            'username': user.username,
            'password': 'testpassword',
        }
        response = self.client.post(url, data)
        self.assertFalse(self.client.login(username='testuser', password='testpassword'))

class TestProfile(TestCase):
    def test_profile(self):
        user = create_test_user_in_db()
        self.client.login(username='testuser', password='testpassword')

        url = reverse('accounts:profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Submit the profile form with incomplete data
        data = {
            'email': 'new_test@example.com',
            'username': 'new_testuser',
            'language': 'en',
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, '/')
        self.assertEqual(response.status_code, 302)

        # Check that the user can log in with the new username
        url = reverse('accounts:login')
        response = self.client.get(url)
        data = {
            'username': 'new_testuser',
            'password': 'testpassword',
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, '/')
        self.assertTrue(self.client.login(username='new_testuser', password='testpassword'))

class TestTermsOfService(TestCase):
    def setUp(self):
        self.terms = TermsOfService.objects.create(
            title='Terms of service',
            content='Terms of service content',
        )
        self.url = reverse('accounts:terms')

    def test_terms_of_service(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_terms_of_service_only_1(self):
        """
        Test that only one terms of service can be created.
        """
        with self.assertRaises(IntegrityError):
            TermsOfService.objects.create(
                title="Second terms of service",
                content="Second terms of service content"
            )

class TestPrivacyPolicy(TestCase):
    def setUp(self):
        self.privacy = PrivacyPolicy.objects.create(
            title='Privacy policy',
            content='Privacy policy content',
        )
        self.url = reverse('accounts:privacy')

    def test_privacy_policy(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_privacy_policy_only_1(self):
        """
        Test that only one privacy policy can be created.
        """
        with self.assertRaises(IntegrityError):
            PrivacyPolicy.objects.create(
                title='second Privacy policy',
                content='Second Privacy policy content',
            )

def create_test_user_in_db(
    username='testuser',
    email='test@example.com',
    password='testpassword',
    is_active=True,
):
    if CustomUser.objects.filter(username=username).exists():
        return CustomUser.objects.get(username=username)
    user = CustomUser.objects.create_user(
        username=username,
        email=email,
        password=password,
        is_active=is_active,
    )
    return user