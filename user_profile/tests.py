from django.test import TestCase, Client
from .forms import EditProfileForm
from django.contrib.auth import get_user_model
from web.models import CustomUser
from django.urls import reverse

CustomUser = get_user_model()


class EditProfileFormTestCase(TestCase):
    def test_edit_profile_form_address_not_required_for_restaurant(self):
        user = CustomUser.objects.create(
            email='user@example.com',
            username='user_user',
            name='User Name',
            phone_number='123456789',
            address='User Address',
            user_type='user'
        )

        form_data = {
            'username': 'new_username',
            'name': 'New Name',
            'phone_number': '987654321',
            'user_type': 'restaurant',
        }

        form = EditProfileForm(data=form_data, instance=user)

        if not form.is_valid():
            print(form.errors)

        self.assertFalse(form.is_valid())

