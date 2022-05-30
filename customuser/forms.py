from dataclasses import field
from django.contrib.auth.forms import UserCreationForm
from .models import User,Profile
from django import forms  #recently addedd for login function

# authentication/forms.py
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=63)
    password = forms.CharField(max_length=63, widget=forms.PasswordInput)

class CustomerSignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')  
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')  

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_customer = True
        if commit:
            user.save()
        return user

class SellerSignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required') 
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_seller = True
        if commit:
            user.save()
        return user


class UpdateProfile(forms.ModelForm):
    class Meta:
        model= Profile
        fields = ['desc','locations','pin','job']

