from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth import get_user_model

from django import forms

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username','email']

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError("Email already in use")
        return data
    def clean_username(self):
        data = self.cleaned_data['username']
        if len(data) < 5:
            raise forms.ValidationError('Length of username must be greater than 4 digits')
        return data


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email']
    
    def clean_email(self):
        User = get_user_model()
        data = self.cleaned_data['email']
        query = User.objects.exclude(id = self.instance.id).filter(email=data)
        if query.exists():
            raise forms.ValidationError('Email is already in use')
        return data
    
    def clean_username(self):
        data = self.cleaned_data['username']
        if len(data) < 5:
            raise forms.ValidationError('Lenght of username must be greater than 4 digits')
        return data