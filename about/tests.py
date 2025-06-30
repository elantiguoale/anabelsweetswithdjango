# pylint: disable=no-member
"""Tests for the about app (models, forms, views, integration)."""
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Post, CakeSubmission, Order
from .forms import CakeSubmissionForm, OrderForm
from datetime import date, timedelta
import os
from io import BytesIO
from PIL import Image


class PostModelTest(TestCase):
    """Test cases for the Post model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
    def test_post_creation(self):
        """Test creating a post"""
        # pylint: disable=no-member
        post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            author=self.user,
            content='This is a test post content.',
            status='published'
        )
        self.assertEqual(post.title, 'Test Post')
        self.assertEqual(post.author, self.user)
        self.assertEqual(post.status, 'published')
        
    def test_post_str_representation(self):
        """Test the string representation of a post"""
        # pylint: disable=no-member
        post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            author=self.user,
            content='Test content'
        )
        expected = f"Test Post | written by {self.user}"
        self.assertEqual(str(post), expected)


class CakeSubmissionModelTest(TestCase):
    """Test cases for the CakeSubmission model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
    def test_cake_submission_creation(self):
        """Test creating a cake submission"""
        # pylint: disable=no-member
        submission = CakeSubmission.objects.create(
            user=self.user,
            cake_name='Test Cake',
            description='A delicious test cake',
            approval_status='pending'
        )
        self.assertEqual(submission.cake_name, 'Test Cake')
        self.assertEqual(submission.user, self.user)
        self.assertEqual(submission.approval_status, 'pending')
        
    def test_cake_submission_str_representation(self):
        """Test the string representation of a cake submission"""
        # pylint: disable=no-member
        submission = CakeSubmission.objects.create(
            user=self.user,
            cake_name='Test Cake',
            description='Test description',
            approval_status='approved'
        )
        expected = f"Test Cake by {self.user} - approved"
        self.assertEqual(str(submission), expected)
        
    def test_is_approved_property(self):
        """Test the is_approved property"""
        # pylint: disable=no-member
        submission = CakeSubmission.objects.create(
            user=self.user,
            cake_name='Test Cake',
            description='Test description',
            approval_status='approved'
        )
        self.assertTrue(submission.is_approved)
        
        submission.approval_status = 'pending'
        submission.save()
        self.assertFalse(submission.is_approved)


class OrderModelTest(TestCase):
    """Test cases for the Order model"""
    
    def setUp(self):
        self.event_date = date.today() + timedelta(days=7)
        
    def test_order_creation(self):
        """Test creating an order"""
        # pylint: disable=no-member
        order = Order.objects.create(
            customer_name='John Doe',
            customer_email='john@example.com',
            customer_phone='+46701234567',
            cake_flavor='chocolate',
            cake_size='20',
            design_description='A beautiful chocolate cake',
            event_date=self.event_date,
            event_type='Birthday'
        )
        self.assertEqual(order.customer_name, 'John Doe')
        self.assertEqual(order.cake_flavor, 'chocolate')
        self.assertEqual(order.status, 'pending')
        
    def test_order_str_representation(self):
        """Test the string representation of an order"""
        # pylint: disable=no-member
        order = Order.objects.create(
            customer_name='John Doe',
            customer_email='john@example.com',
            customer_phone='+46701234567',
            cake_flavor='chocolate',
            cake_size='20',
            design_description='Test design',
            event_date=self.event_date,
            event_type='Birthday'
        )
        expected = f"Order #{order.id} - John Doe - chocolate - pending"
        self.assertEqual(str(order), expected)
        
    def test_is_urgent_property(self):
        """Test the is_urgent property"""
        # Test urgent order (within 3 days)
        urgent_date = date.today() + timedelta(days=2)
        # pylint: disable=no-member
        urgent_order = Order.objects.create(
            customer_name='John Doe',
            customer_email='john@example.com',
            customer_phone='+46701234567',
            cake_flavor='chocolate',
            cake_size='20',
            design_description='Test design',
            event_date=urgent_date,
            event_type='Birthday'
        )
        self.assertTrue(urgent_order.is_urgent)
        
        # Test non-urgent order (more than 3 days)
        non_urgent_date = date.today() + timedelta(days=5)
        # pylint: disable=no-member
        non_urgent_order = Order.objects.create(
            customer_name='Jane Doe',
            customer_email='jane@example.com',
            customer_phone='+46701234568',
            cake_flavor='strawberry',
            cake_size='25',
            design_description='Test design',
            event_date=non_urgent_date,
            event_type='Wedding'
        )
        self.assertFalse(non_urgent_order.is_urgent)


class CakeSubmissionFormTest(TestCase):
    """Test cases for the CakeSubmissionForm"""
    
    def test_valid_form(self):
        """Test a valid cake submission form"""
        # Use Pillow to generate a real in-memory image
        image_io = BytesIO()
        image = Image.new('RGB', (1, 1), color='white')
        image.save(image_io, format='PNG')
        image_io.seek(0)
        test_image = SimpleUploadedFile(
            name='test_cake.png',
            content=image_io.read(),
            content_type='image/png'
        )
        
        form_data = {
            'cake_name': 'Test Cake',
            'description': 'A delicious test cake'
        }
        form_files = {
            'image': test_image
        }
        form = CakeSubmissionForm(data=form_data, files=form_files)
        if not form.is_valid():
            print('Form errors:', form.errors)
        self.assertTrue(form.is_valid())
        # Simulate view usage: set user before saving
        user = User.objects.create_user(username='cakeuser', email='cake@example.com', password='cakepass')
        instance = form.save(commit=False)
        instance.user = user
        instance.save()
        self.assertEqual(instance.cake_name, 'Test Cake')
        
    def test_invalid_form_missing_name(self):
        """Test form validation when cake name is missing"""
        minimal_png = (
            b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01'
            b'\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0bIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01'
            b'\x0d\n\x2d\xb4\x00\x00\x00\x00IEND\xaeB`\x82'
        )
        test_image = SimpleUploadedFile(
            name='test_cake.png',
            content=minimal_png,
            content_type='image/png'
        )
        
        form_data = {
            'description': 'A delicious test cake'
        }
        form_files = {
            'image': test_image
        }
        form = CakeSubmissionForm(data=form_data, files=form_files)
        self.assertFalse(form.is_valid())
        self.assertIn('cake_name', form.errors)  # type: ignore


class OrderFormTest(TestCase):
    """Test cases for the OrderForm"""
    
    def setUp(self):
        self.valid_data = {
            'customer_name': 'John Doe',
            'customer_email': 'john@example.com',
            'customer_phone': '+46701234567',
            'cake_flavor': 'chocolate',
            'cake_size': '20',
            'design_description': 'A beautiful chocolate cake',
            'event_date': (date.today() + timedelta(days=5)).isoformat(),
            'event_type': 'Birthday'
        }
        
    def test_valid_order_form(self):
        """Test a valid order form"""
        form = OrderForm(data=self.valid_data)
        self.assertTrue(form.is_valid())
        
    def test_invalid_order_form_missing_required_fields(self):
        """Test form validation when required fields are missing"""
        form_data = {
            'customer_name': 'John Doe',
            'cake_flavor': 'chocolate'
        }
        form = OrderForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('customer_email', form.errors)  # type: ignore
        self.assertIn('design_description', form.errors)  # type: ignore
        
    def test_custom_flavor_validation(self):
        """Test validation for custom flavor description"""
        data = self.valid_data.copy()
        data['cake_flavor'] = 'custom'
        # Missing custom flavor description
        form = OrderForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)  # type: ignore
        
        # With custom flavor description
        data['custom_flavor_description'] = 'A unique vanilla-chocolate mix'
        form = OrderForm(data=data)
        self.assertTrue(form.is_valid())
        
    def test_event_date_validation(self):
        """Test validation for event date (must be at least 3 days in future)"""
        data = self.valid_data.copy()
        # Date too soon (within 3 days)
        data['event_date'] = (date.today() + timedelta(days=2)).isoformat()
        form = OrderForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)  # type: ignore
        
        # Valid date (more than 3 days)
        data['event_date'] = (date.today() + timedelta(days=5)).isoformat()
        form = OrderForm(data=data)
        self.assertTrue(form.is_valid())


class ViewsTest(TestCase):
    """Test cases for views"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
    def test_about_view(self):
        """Test the about view"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)  # type: ignore
        self.assertTemplateUsed(response, 'about/about_me.html')
        
    def test_wall_of_fame_view(self):
        """Test the wall of fame view"""
        response = self.client.get(reverse('wall_of_fame'))
        self.assertEqual(response.status_code, 200)  # type: ignore
        self.assertTemplateUsed(response, 'about/wall_of_fame.html')
        
    def test_submit_cake_view_requires_login(self):
        """Test that submit cake view requires login"""
        response = self.client.get(reverse('submit_cake'))
        self.assertEqual(response.status_code, 302)  # type: ignore # Redirect to login
        
    def test_submit_cake_view_with_login(self):
        """Test submit cake view when user is logged in"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('submit_cake'))
        self.assertEqual(response.status_code, 200)  # type: ignore
        self.assertTemplateUsed(response, 'about/submit_cake.html')
        
    def test_order_cake_view(self):
        """Test the order cake view"""
        response = self.client.get(reverse('order_cake'))
        self.assertEqual(response.status_code, 200)  # type: ignore
        self.assertTemplateUsed(response, 'about/order.html')
        
    def test_my_orders_view_requires_login(self):
        """Test that my orders view requires login"""
        response = self.client.get(reverse('my_orders'))
        self.assertEqual(response.status_code, 302)  # type: ignore # Redirect to login
        
    def test_my_orders_view_with_login(self):
        """Test my orders view when user is logged in"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('my_orders'))
        self.assertEqual(response.status_code, 200)  # type: ignore
        self.assertTemplateUsed(response, 'about/my_orders.html')


class AuthenticationViewsTest(TestCase):
    """Test cases for authentication views"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
    def test_register_view(self):
        """Test user registration"""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register_simple.html')
        
    def test_login_view(self):
        """Test user login"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login_simple.html')
        
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


class IntegrationTest(TestCase):
    """Integration tests for complete workflows"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
    def test_complete_order_workflow(self):
        """Test the complete order workflow"""
        # Place an order
        order_data = {
            'customer_name': 'John Doe',
            'customer_email': 'john@example.com',
            'customer_phone': '+46701234567',
            'cake_flavor': 'chocolate',
            'cake_size': '20',
            'design_description': 'A beautiful chocolate cake',
            'event_date': (date.today() + timedelta(days=5)).isoformat(),
            'event_type': 'Birthday'
        }
        
        response = self.client.post(reverse('order_cake'), order_data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        
        # Check that order was created
        order = Order.objects.get(customer_email='john@example.com')
        self.assertEqual(order.customer_name, 'John Doe')
        self.assertEqual(order.cake_flavor, 'chocolate')
        
    def test_my_orders_workflow(self):
        """Test the my orders workflow"""
        # Create an order for the logged-in user
        order = Order.objects.create(
            customer_name='Test User',
            customer_email='test@example.com',  # Same as user email
            customer_phone='+46701234567',
            cake_flavor='strawberry',
            cake_size='25',
            design_description='Test cake design',
            event_date=date.today() + timedelta(days=7),
            event_type='Birthday'
        )
        
        # Login and check my orders
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('my_orders'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Strawberry')  # Capitalized flavor name
        self.assertContains(response, 'Birthday')  # Event type is always shown
