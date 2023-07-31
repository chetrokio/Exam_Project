from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .views import ProfileInfoView, ProfileEditView, ChangePasswordView, DeleteProfileView, ConfirmDeleteView, \
    UserProfileView

urlpatterns = [
    path('', UserProfileView.as_view(), name='user_profile'),
    path('info/', ProfileInfoView.as_view(), name='profile_info'),
    path('edit/', ProfileEditView.as_view(), name='profile_edit'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('delete/', DeleteProfileView.as_view(), name='delete_profile'),
    path('confirm-delete/', ConfirmDeleteView.as_view(), name='confirm_delete'),
]