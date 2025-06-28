from django import forms
from .models import CakeSubmission, Order

class CakeSubmissionForm(forms.ModelForm):
    """
    Form for users to submit their cake pictures to the Wall of Fame
    """
    class Meta:
        model = CakeSubmission
        fields = ['cake_name', 'description', 'image']
        widgets = {
            'cake_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'What\'s your cake called?'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Tell us about your cake! What makes it special?'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cake_name'].label = "Cake Name"
        self.fields['description'].label = "Description"
        self.fields['image'].label = "Cake Photo"
        
        # Add help text
        self.fields['cake_name'].help_text = "Give your cake a creative name!"
        self.fields['description'].help_text = "Share what makes your cake special"
        self.fields['image'].help_text = "Upload a clear photo of your cake (JPG, PNG, GIF)"


class OrderForm(forms.ModelForm):
    """
    Form for customers to place cake orders
    """
    class Meta:
        model = Order
        fields = [
            'customer_name', 'customer_email', 'customer_phone',
            'cake_flavor', 'custom_flavor_description', 'cake_size',
            'design_description', 'special_requests', 'event_date', 'event_type'
        ]
        widgets = {
            'customer_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your full name'
            }),
            'customer_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@example.com'
            }),
            'customer_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+46 70 123 4567'
            }),
            'cake_flavor': forms.Select(attrs={
                'class': 'form-control'
            }),
            'custom_flavor_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe your custom flavor in detail...'
            }),
            'cake_size': forms.Select(attrs={
                'class': 'form-control'
            }),
            'design_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe your dream cake design, colors, theme, decorations...'
            }),
            'special_requests': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Any dietary requirements, allergies, or special instructions...'
            }),
            'event_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'min': '2024-01-01'
            }),
            'event_type': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Birthday, Wedding, Anniversary, Graduation'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set labels
        self.fields['customer_name'].label = "Full Name *"
        self.fields['customer_email'].label = "Email Address *"
        self.fields['customer_phone'].label = "Phone Number *"
        self.fields['cake_flavor'].label = "Cake Flavor *"
        self.fields['custom_flavor_description'].label = "Custom Flavor Description"
        self.fields['cake_size'].label = "Cake Size *"
        self.fields['design_description'].label = "Design Description *"
        self.fields['special_requests'].label = "Special Requests"
        self.fields['event_date'].label = "Event Date *"
        self.fields['event_type'].label = "Event Type *"
        
        # Add help text
        self.fields['custom_flavor_description'].help_text = "Required if you selected 'Custom Flavor'"
        self.fields['cake_size'].help_text = "Select the cake diameter"
        self.fields['event_date'].help_text = "When do you need the cake? (Please allow at least 3 days notice)"
        
        # Set minimum date to today
        from datetime import date
        self.fields['event_date'].widget.attrs['min'] = date.today().isoformat()
    
    def clean(self):
        cleaned_data = super().clean()
        cake_flavor = cleaned_data.get('cake_flavor')
        custom_flavor_description = cleaned_data.get('custom_flavor_description')
        event_date = cleaned_data.get('event_date')
        
        # Check if custom flavor description is provided when custom flavor is selected
        if cake_flavor == 'custom' and not custom_flavor_description:
            raise forms.ValidationError(
                "Please provide a description for your custom flavor."
            )
        
        # Check if event date is at least 3 days in the future
        if event_date:
            from datetime import date, timedelta
            min_date = date.today() + timedelta(days=3)
            if event_date < min_date:
                raise forms.ValidationError(
                    f"Please allow at least 3 days notice. Earliest available date is {min_date.strftime('%B %d, %Y')}."
                )
        
        return cleaned_data 