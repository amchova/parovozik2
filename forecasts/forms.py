from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Forecast

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username__iexact=username).exists(): raise forms.ValidationError('Пользователь с таким именем уже существует.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email__iexact=email).exists(): raise forms.ValidationError('Этот email уже зарегистрирован.')
        return email

class AdminCreateUserForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')
    is_staff = forms.BooleanField(required=False, label='Сделать администратором')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'is_staff']

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username__iexact=username).exists(): raise forms.ValidationError('Пользователь с таким именем уже существует.')
        return username

class ForecastForm(forms.ModelForm):
    class Meta:
        model = Forecast
        fields = ['title', 'category', 'description', 'region', 'price', 'file']
        widgets = {'description': forms.Textarea(attrs={'rows': 4}),}