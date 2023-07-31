from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.views.generic.edit import DeleteView

from web.forms import CustomUser
from .forms import EditProfileForm
from .models import Profile


class UserProfileView(LoginRequiredMixin, View):
    template_name = 'profile/user_profile.html'

    def get(self, request):
        return render(request, self.template_name)


class ProfileInfoView(LoginRequiredMixin, View):
    template_name = 'profile/profile_info.html'
    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        return render(request, self.template_name, {'profile': profile})


class ProfileEditView(LoginRequiredMixin, View):
    template_name = 'profile/profile_edit.html'

    def get(self, request):
        profile = CustomUser.objects.get(pk=request.user.pk)
        form = EditProfileForm(instance=profile)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        profile = CustomUser.objects.get(pk=request.user.pk)
        form = EditProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_info')
        return render(request, self.template_name, {'form': form})


class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'profile/change_password.html'
    success_url = '/profile/'


class DeleteProfileView(LoginRequiredMixin, DeleteView):
    template_name = 'profile/delete_profile.html'
    success_url = '/profile/'
    def get_object(self):
        return self.request.user


class ConfirmDeleteView(LoginRequiredMixin, View):
    template_name = 'confirm_delete.html'
    def post(self, request):
        user = request.user
        user.delete()
        return redirect('home')