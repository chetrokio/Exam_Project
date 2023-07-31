from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import View, CreateView, ListView, CreateView, DetailView
from django.views.generic.base import TemplateView
from user_profile.models import Profile
from .forms import UserRegistrationForm, MenuForm
from .models import CustomUser, Review, Order, Menu
from django.shortcuts import render, redirect, reverse,  get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def WikipediaStatisticsView(request):
    data = {
        'summary': 'Food waste refers to the discarding or loss of edible food that could have been consumed by humans or animals. It is a significant global issue with considerable environmental, social, and economic impacts.',
        'average_waste_per_person': 'Approximately 150 kilograms per year',
        'countries_with_most_waste': ['United States', 'China', 'India', 'Brazil', 'Russia'],
        'food_waste_impact': 'Food waste contributes to approximately 8% of global greenhouse gas emissions.',
        'food_waste_cost': 'Food waste costs the global economy an estimated $940 billion annually.',
        'food_waste_reduction': 'A 50% reduction in food waste could save up to 2 billion tons of food and feed an additional 3 billion people.',
        'food_waste_recycling': 'Approximately 15% of food waste is recycled into compost or bioenergy.',
        'food_loss_in_supply_chain': 'Around 14% of food is lost in the supply chain before reaching consumers.',
    }

    return render(request, 'leftovers.html', context=data)


def index(request):
    return render(request, "index.html")


class CustomLoginView(LoginView):
    template_name = 'login.html'
    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password.')
        return super().form_invalid(form)

    def get_success_url(self):
        if self.request.user.last_login is None:
            return reverse('edit_profile')
        else:
            if self.request.user.user_type == 'restaurant':
                return reverse('add_menu_option')
            else:
                return reverse('view_menu_options')


class CustomLogoutView(LogoutView):
    next_page = 'home'


class UserRegistrationView(CreateView):
    model = CustomUser
    form_class = UserRegistrationForm
    template_name = 'user_register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        profile = Profile.objects.create(user=user)
        return super().form_valid(form)


@login_required
def view_menu_options(request):
    menu_items = Menu.objects.all()
    return render(request, 'view_menu_options.html', {'menu_items': menu_items})


@login_required
def add_menu_options(request):
    if request.user.user_type == 'restaurant':
        if request.method == 'POST':
            form = MenuForm(request.POST)
            if form.is_valid():
                menu_item = form.save(commit=False)
                menu_item.restaurant = request.user
                menu_item.save()
                return redirect('view_menu_options')
        else:
            form = MenuForm()
        return render(request, 'add_menu_options.html', {'form': form})
    else:
        return redirect('home')


class MenuOrderView(View):
    def post(self, request, menu_item_id):
        try:
            menu_item = Menu.objects.get(pk=menu_item_id)
            menu_item.delete()
            return redirect('order_confirmation')
        except Menu.DoesNotExist:
            return redirect('error')


class OrderConfirmationView(TemplateView):
    template_name = 'order_confirmation.html'


class ErrorView(TemplateView):
    template_name = 'error.html'
