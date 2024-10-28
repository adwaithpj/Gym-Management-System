# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import GymAdmin

class GymAdminCreationForm(UserCreationForm):
    # username = forms.CharField(required=True,max_length=30,help_text='Required')
    # username = None
    first_name = forms.CharField(max_length=30, required=True, help_text='Required')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required')
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Inform a valid email address.')
    phone_number = forms.CharField(max_length=10, required=True, help_text='Required')
    is_staff = forms.BooleanField(label='Staff status', required=False)
    class Meta:
        model = GymAdmin
        fields = ('first_name', 'last_name',  'email', 'phone_number', 'password1', 'password2','is_staff')
    
    def __init__(self, *args, **kwargs):
        super(GymAdminCreationForm, self).__init__(*args, **kwargs)
        placeholders = {
            # 'username': 'Enter your username',
            'first_name': 'Enter your First name',
            'last_name': 'Enter your Last Name',
            'email': 'Enter your Email',
            'phone_number': 'Enter your Phone number',
            'password1': 'Enter your password',
            'password2': 'Retype your password'
        }
        
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'rounded-lg shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'
            if field in placeholders:
                self.fields[field].widget.attrs['placeholder'] = placeholders[field]
            
            if field == 'is_staff':
                self.fields[field].widget.attrs['class'] = 'form-check-input' 
            

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number.isdigit() or len(phone_number) != 10:
            raise forms.ValidationError("Enter a valid 10-digit phone number.")
        return phone_number

    def clean(self):
        cleaned_data = super().clean()
        # username = cleaned_data.get('username')
        phone_number = cleaned_data.get('phone_number')
        
        # Check if username already exists
        email = self.cleaned_data.get('email')
        if GymAdmin.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists.")
        # if GymAdmin.objects.filter(username=username).exists():
            # self.add_error('username', 'This username is already taken. Please choose a different one.')

        # Check if phone number already exists
        if GymAdmin.objects.filter(phone_number=phone_number).exists():
            self.add_error('phone_number', 'This phone number is already registered. Please use a different one.')
            
class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=254, widget=forms.TextInput(attrs={'class': 'rounded-lg shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline', 'placeholder': 'Email'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'rounded-lg shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline', 'placeholder':'Password'}))
    
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if not username:
            self.add_error('username', 'Username is required')
        if not password:
            self.add_error('password', 'Password is required')
        
        return cleaned_data


class GoogleForm(forms.Form):
    phone_number = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class': 'rounded-lg shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline input', 'placeholder': 'Phone Number'}))
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number.isdigit() or len(phone_number) != 10:
            raise forms.ValidationError("Enter a valid 10-digit phone number.")
        return phone_number
    
    def clean(self):
        cleaned_data = super().clean()
        phone_number = cleaned_data.get('phone_number')

        # Check if phone number already exists
        if GymAdmin.objects.filter(phone_number=phone_number).exists():
            self.add_error('phone_number', 'This phone number is already registered. Please use a different one.')