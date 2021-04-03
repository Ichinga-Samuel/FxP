from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm, PasswordResetForm, \
    SetPasswordForm

attrs = {'class': 'form-control', 'placeholder': ''}


class UserLoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(attrs=attrs))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': ''}))


class UserRegistrationForm(UserCreationForm):

    username = forms.CharField(max_length=30, required=False, help_text='Enter a Preferred Username',
                               widget=forms.TextInput(attrs=attrs))

    email = forms.EmailField(max_length=254, help_text='Enter a valid email address.',
                             widget=forms.EmailInput(attrs=attrs))
    password1 = forms.CharField(help_text='Your password must be 8-20 characters long, and must contain'
                                          'numbers, lower and upper case letters',
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': ''}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': ''}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )


class PasswordReset(PasswordResetForm):

    email = forms.EmailField(max_length=254, help_text='Enter the email address you registered with.',
                             widget=forms.EmailInput(attrs=attrs))


class PasswordChange(SetPasswordForm):

    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs=attrs),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )

    new_password2 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs=attrs),
    )
