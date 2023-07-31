from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from web.models import Menu

CustomUser = get_user_model()


class UserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        validators=[validate_password],
        help_text=_("Your password must contain at least 8 characters, cannot be entirely numeric, and cannot be too common."),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'user_type']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = _('Email')
        self.fields['username'].widget.attrs['placeholder'] = _('Username')
        self.fields['user_type'].widget.attrs['placeholder'] = _('User Type')


class CustomLoginForm(AuthenticationForm):
    pass


class CustomUserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'user_type', 'name', 'phone_number', 'address']


class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['dish_name', 'description', 'price']