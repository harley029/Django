from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm): 
    password = forms.CharField(label='Password', widget=forms.PasswordInput) 
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.') 
        return cd['password2']

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('This Email is already in use.') 
        return data

    def save(self, commit=True):
        user = super().save(commit=False)
        # Используем set_password для хеширования пароля
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
