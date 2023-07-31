from django import forms
from web.models import CustomUser


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'name', 'phone_number', 'address']