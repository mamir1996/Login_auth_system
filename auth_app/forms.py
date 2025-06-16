from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
import re
class SignupForm(forms.Form):
    user_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username'})
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter First Name'})
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Last Name'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'})
    )
    # phone_num = forms.IntegerField(widget=forms.NumberInput(attrs={
    #     'class': 'form-control',
    #     'placeholder': 'Enter your phone number'
    # })
# )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'})
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'})
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('user_name')
        email = cleaned_data.get('email')
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        # Username validations
        if username:
            if User.objects.filter(username=username).exists():
                self.add_error('user_name', "Username already exists.")
            if len(username) < 3:
                self.add_error('user_name', "Username must be at least 3 characters long.")

        # First name and last name validations
        if first_name and len(first_name) < 3:
            self.add_error('first_name', "First name must be at least 2 characters.")
        if last_name and len(last_name) < 3:
            self.add_error('last_name', "Last name must be at least 2 characters.")

        # Email validations
        if email and User.objects.filter(email=email).exists():
            self.add_error('email', "Email already registered.")

        # Password validations
        if password:
            if len(password) < 8:
                self.add_error('password', "Password must be at least 8 characters.")
            if not re.search(r'[A-Z]', password):
                self.add_error('password', "Password must contain at least one uppercase letter.")
            if not re.search(r'[a-z]', password):
                self.add_error('password', "Password must contain at least one lowercase letter.")
            if not re.search(r'\d', password):
                self.add_error('password', "Password must contain at least one number.")
            if not re.search(r'[!@#$%^&*()_+{}\[\]:;<>,.?~\\/-]', password):
                self.add_error('password', "Password must include at least one special character.")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match!")


class SigninForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'})
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("Invalid username or password.")
            self.user = user  # Save the user
        return cleaned_data
