from django import forms
from .models import UserProfile

# forms.py
from allauth.account.forms import SignupForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'phone', 'address']


class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Initialize Crispy Forms helper
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'space-y-6'
        
        # Define a custom layout with widget classes
        self.helper.layout = Layout(
            Field('username', css_class='appearance-none border rounded w-full py-2 px-3 text-gray-700'),
            Field('email', css_class='appearance-none border rounded w-full py-2 px-3 text-gray-700'),
            Field('password1', css_class='appearance-none border rounded w-full py-2 px-3 text-gray-700'),
            Field('password2', css_class='appearance-none border rounded w-full py-2 px-3 text-gray-700'),
            Div(
                Submit('signup', 'Sign Up', css_class='w-full bg-blue-600 text-white py-3 rounded-xl text-lg font-semibold hover:bg-blue-700 focus:outline-none focus:ring-4 focus:ring-blue-300 transition duration-300'),
                css_class='mt-4'
            )
        )
