from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.password_validation import validate_password

from web.models import Menu, Review
from django.utils.translation import gettext_lazy as _

CustomUser = get_user_model()

class UserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        validators=[validate_password],
        help_text=_("Your password must contain at least 8 characters,"
                    " cannot be entirely numeric, and cannot be too common."),
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
        self.fields["email"].widget.attrs["placeholder"] = _("Email")
        self.fields["username"].widget.attrs["placeholder"] = _("Username")
        self.fields["user_type"].widget.attrs["placeholder"] = _("User Type")


class CustomLoginForm(AuthenticationForm):
    pass


class CustomUserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["username", "email", "user_type", "name", "phone_number", "address"]

    def clean_address(self):
        address = self.cleaned_data.get('address')

        if self.instance.user_type == 'user' and not address:
            raise forms.ValidationError("Please provide a valid address.")

        return address


class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['restaurant', 'dish_name', 'quantity', 'description', 'price']

    def clean(self):
        cleaned_data = super().clean()
        restaurant = cleaned_data.get('restaurant')

        if restaurant.user_type != 'restaurant':
            raise forms.ValidationError("Only restaurants can add menu items.")

        if not restaurant.name:
            raise forms.ValidationError("Please provide a restaurant name.")

        return cleaned_data


class OrderForm(forms.Form):
    def __init__(self, menu_items, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for menu_item in menu_items:
            field_name = f"quantity_{menu_item.pk}"
            self.fields[field_name] = forms.IntegerField(
                label=menu_item.dish_name,
                min_value=0,
                max_value=menu_item.quantity,
                widget=forms.NumberInput(attrs={'class': 'form-control'}),
            )


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']