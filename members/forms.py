from django import forms
from .models import GymMembers

FORMS_CLASS_NAME = 'rounded-lg shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'


class GymMembersForm(forms.ModelForm):
    class Meta:
        model = GymMembers
        fields = [
            'name', 'email', 'phone_number', 'address', 'city',
            'sub_type', 'pay_method', 'user_profile_image', 'is_active'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': f'input {FORMS_CLASS_NAME}', 'placeholder': 'Name', 'required': True}),
            'email': forms.EmailInput(attrs={'class': f'input {FORMS_CLASS_NAME}', 'placeholder': 'Email', 'required': True}),
            'phone_number': forms.TextInput(attrs={'class': f'input {FORMS_CLASS_NAME}', 'placeholder': 'Phone Number', 'required': True}),
            'address': forms.TextInput(attrs={'class': f'input {FORMS_CLASS_NAME}', 'placeholder': 'Address', 'required': True}),
            'city': forms.TextInput(attrs={'class': f'input {FORMS_CLASS_NAME}', 'placeholder': 'City', 'required': True}),
            'sub_type': forms.Select(attrs={'class': f'input {FORMS_CLASS_NAME}', 'required': True}),
            'pay_method': forms.Select(attrs={'class': f'input {FORMS_CLASS_NAME}', 'required': True}),
            'user_profile_image': forms.FileInput(attrs={'accept': 'image/*', 'capture':'camera'})
            }