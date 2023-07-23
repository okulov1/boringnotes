from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth.models import User


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'login'
    }))

    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'email@example.com'
    }))

    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'password'
    }))

    password2 = forms.CharField(label='Пароль (повторить)', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'password'
    }))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'login'
    }))

    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'password'
    }))


class ContactForm(forms.Form):
    title = forms.CharField(max_length=200, label='Тема', widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    content = forms.CharField(label='Текст', widget=forms.Textarea(attrs={
        'cols': 60,
        'rows': 10,
        'class': 'form-control'
    }))


class RedactNoteForm(forms.Form):
    title = forms.CharField(max_length=200, label='Заголовок', widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

    content = forms.CharField(label='Текст', widget=forms.Textarea(attrs={
        'class': 'form-control',
        'rows': 26
    }))

    is_published = forms.BooleanField(required=False, label='Могут читать все', widget=forms.CheckboxInput(attrs={
        'class': 'form-check-input'
    }))
