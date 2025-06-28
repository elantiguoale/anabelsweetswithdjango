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

