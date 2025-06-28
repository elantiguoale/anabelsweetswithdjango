from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    """
    Custom registration form that includes email as a required field
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        help_text='Required. Enter a valid email address.'
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def clean_email(self):
        """
        Validate that the email is unique
        """
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is already in use.')
        return email
    
    def save(self, commit=True):
        """
        Save the user with the email
        """
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user 