from django import forms
from .models import CakeSubmission

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