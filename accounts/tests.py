from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import CustomUserCreationForm


class CustomUserCreationFormTest(TestCase):
    """Test cases for the CustomUserCreationForm"""
    
    def test_valid_registration_form(self):
        """Test a valid user registration form"""
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        
    def test_invalid_registration_form_mismatched_passwords(self):
        """Test form validation when passwords don't match"""
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpass123',
            'password2': 'differentpass'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
        
    def test_invalid_registration_form_missing_email(self):
        """Test form validation when email is missing"""
        form_data = {
            'username': 'testuser',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        
    def test_invalid_registration_form_duplicate_username(self):
        """Test form validation when username already exists"""
        # Create a user first
        User.objects.create_user(
            username='existinguser',
            email='existing@example.com',
            password='testpass123'
        )
        
        # Try to create another user with same username
        form_data = {
            'username': 'existinguser',
            'email': 'new@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        
    def test_invalid_registration_form_duplicate_email(self):
        """Test form validation when email already exists"""
        # Create a user first
        User.objects.create_user(
            username='user1',
            email='test@example.com',
            password='testpass123'
        )
        
        # Try to create another user with same email
        form_data = {
            'username': 'user2',
            'email': 'test@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)


class AuthenticationViewsTest(TestCase):
    """Test cases for authentication views"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
    def test_register_view_get(self):
        """Test GET request to register view"""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register_simple.html')
        
    def test_register_view_post_valid(self):
        """Test POST request to register view with valid data"""
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newpass123',
            'password2': 'newpass123'
        }
        response = self.client.post(reverse('register'), form_data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        
        # Check that user was created
        user = User.objects.get(username='newuser')
        self.assertEqual(user.email, 'newuser@example.com')
        
    def test_register_view_post_invalid(self):
        """Test POST request to register view with invalid data"""
        form_data = {
            'username': 'newuser',
            'email': 'invalid-email',
            'password1': 'newpass123',
            'password2': 'differentpass'
        }
        response = self.client.post(reverse('register'), form_data)
        self.assertEqual(response.status_code, 200)  # Stay on form page
        self.assertTemplateUsed(response, 'accounts/register_simple.html')
        
    def test_login_view_get(self):
        """Test GET request to login view"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login_simple.html')
        
    def test_login_view_post_valid(self):
        """Test POST request to login view with valid credentials"""
        form_data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(reverse('login'), form_data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        
    def test_login_view_post_invalid(self):
        """Test POST request to login view with invalid credentials"""
        form_data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(reverse('login'), form_data)
        self.assertEqual(response.status_code, 200)  # Stay on form page
        self.assertTemplateUsed(response, 'accounts/login_simple.html')
        
    def test_logout_view(self):
        """Test logout view"""
        # Login first
        self.client.login(username='testuser', password='testpass123')
        
        # Test logout
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Redirect after logout
        
    def test_profile_view_requires_login(self):
        """Test that profile view requires login"""
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        
    def test_profile_view_with_login(self):
        """Test profile view when user is logged in"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile_simple.html')
        self.assertContains(response, 'testuser')


class UserModelTest(TestCase):
    """Test cases for User model functionality"""
    
    def test_user_creation(self):
        """Test creating a user"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpass123'))
        
    def test_user_authentication(self):
        """Test user authentication"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Test correct password
        self.assertTrue(user.check_password('testpass123'))
        
        # Test incorrect password
        self.assertFalse(user.check_password('wrongpassword'))
        
    def test_user_str_representation(self):
        """Test the string representation of a user"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.assertEqual(str(user), 'testuser')


class AuthenticationWorkflowTest(TestCase):
    """Integration tests for complete authentication workflows"""
    
    def setUp(self):
        self.client = Client()
        
    def test_complete_registration_login_logout_workflow(self):
        """Test the complete user registration, login, and logout workflow"""
        # Step 1: Register a new user
        register_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newpass123',
            'password2': 'newpass123'
        }
        response = self.client.post(reverse('register'), register_data)
        self.assertEqual(response.status_code, 302)
        
        # Step 2: Login with the new user
        login_data = {
            'username': 'newuser',
            'password': 'newpass123'
        }
        response = self.client.post(reverse('login'), login_data)
        self.assertEqual(response.status_code, 302)
        
        # Step 3: Access profile (should work when logged in)
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'newuser')
        
        # Step 4: Logout
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        
        # Step 5: Try to access profile (should redirect to login)
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)
        
    def test_duplicate_registration_handling(self):
        """Test handling of duplicate username/email during registration"""
        # Create first user
        User.objects.create_user(
            username='existinguser',
            email='existing@example.com',
            password='testpass123'
        )
        
        # Try to register with same username
        register_data = {
            'username': 'existinguser',
            'email': 'different@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        response = self.client.post(reverse('register'), register_data)
        self.assertEqual(response.status_code, 200)  # Form errors, stay on page
        
        # Try to register with same email
        register_data = {
            'username': 'differentuser',
            'email': 'existing@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        response = self.client.post(reverse('register'), register_data)
        self.assertEqual(response.status_code, 200)  # Form errors, stay on page
