from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterOperator(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text="Required. Add a valid email address")
    class Meta:
        model = User
        fields = ('email', "username","first_name", "last_name", "password1","password2")

