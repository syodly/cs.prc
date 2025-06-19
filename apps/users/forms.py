from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'password1', 'password2')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'phone') 