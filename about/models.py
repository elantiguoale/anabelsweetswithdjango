from django.db import models
from django.contrib.auth.models import User

STATUS = (("draft", "Draft"), ("published", "Published"))

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="about_me"
    )
    content = models.TextField(default="")
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS, default="draft")
    excerpt = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f"{self.title} | written by {self.author}"


class CakeSubmission(models.Model):
    """
    Model for user-submitted cake pictures for the Wall of Fame
    """
    APPROVAL_STATUS = (
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cake_submissions')
    cake_name = models.CharField(max_length=200, help_text="What's your cake called?")
    description = models.TextField(help_text="Tell us about your cake!")
    image = models.ImageField(upload_to='cake_submissions/', help_text="Upload a photo of your cake")
    submission_date = models.DateTimeField(auto_now_add=True)
    approval_status = models.CharField(max_length=10, choices=APPROVAL_STATUS, default='pending')
    admin_notes = models.TextField(blank=True, help_text="Admin notes (not visible to user)")
    
    class Meta:
        ordering = ['-submission_date']
        verbose_name = "Cake Submission"
        verbose_name_plural = "Cake Submissions"
    
    def __str__(self):
        return f"{self.cake_name} by {self.user} - {self.approval_status}"
    
    @property
    def is_approved(self):
        return self.approval_status == 'approved'
    
    @property
    def is_pending(self):
        return self.approval_status == 'pending'


class Order(models.Model):
    """
    Model for cake orders
    """
    ORDER_STATUS = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('ready', 'Ready for Pickup'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    CAKE_FLAVORS = (
        ('chocolate', 'Chocolate'),
        ('strawberry', 'Strawberry'),
        ('tiramisu', 'Tiramisu'),
        ('oreo', 'Oreo'),
        ('lime', 'Lime'),
        ('dulce_de_leche', 'Dulce de Leche'),
        ('custom', 'Custom Flavor'),
    )
    
    CAKE_SIZES = (
        ('15', '15 cm (6 inch)'),
        ('20', '20 cm (8 inch)'),
        ('25', '25 cm (10 inch)'),
        ('30', '30 cm (12 inch)'),
    )
    
    # Customer Information
    customer_name = models.CharField(max_length=200)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)
    
    # Order Details
    cake_flavor = models.CharField(max_length=20, choices=CAKE_FLAVORS)
    custom_flavor_description = models.TextField(blank=True, help_text="Describe your custom flavor if selected")
    cake_size = models.CharField(max_length=2, choices=CAKE_SIZES, help_text="Cake diameter in centimeters")
    
    # Design and Special Requests
    design_description = models.TextField(help_text="Describe your desired cake design")
    special_requests = models.TextField(blank=True, help_text="Any special requests or dietary requirements")
    
    # Event Details
    event_date = models.DateField(help_text="When do you need the cake?")
    event_type = models.CharField(max_length=100, help_text="e.g., Birthday, Wedding, Anniversary, etc.")
    
    # Pricing and Status
    estimated_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, help_text="Estimated price in SEK")
    final_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, help_text="Final price in SEK")
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending')
    
    # Timestamps
    order_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    # Admin notes
    admin_notes = models.TextField(blank=True, help_text="Internal notes (not visible to customer)")
    
    class Meta:
        ordering = ['-order_date']
        verbose_name = "Order"
        verbose_name_plural = "Orders"
    
    def __str__(self):
        return f"Order #{self.id} - {self.customer_name} - {self.cake_flavor} - {self.status}"
    
    @property
    def is_urgent(self):
        """Check if order is urgent (less than 3 days away)"""
        from datetime import date, timedelta
        return self.event_date <= date.today() + timedelta(days=3)

