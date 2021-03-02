from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Account


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['image']


class LoginForm(forms.Form):
    # username = forms.CharField(widget=forms.TextInput(attrs={'placeholer: username'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'email'}))
    password = forms.CharField(widget=forms.PasswordInput())

    # city = forms.CharField()
    # check_me_out = forms.BooleanField(required=False)
