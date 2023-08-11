from asgiref.sync import sync_to_async
from django.contrib.auth.views import LoginView, LogoutView
from django.http.response import Http404
from django.views.generic import View, CreateView, ListView, CreateView, DetailView
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy
from user_profile.models import Profile
from .forms import MenuForm, OrderForm, CustomUser, UserRegistrationForm, ReviewForm
from .models import Review, Order, Menu
from django.shortcuts import render, redirect, reverse,  get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def index(request):
    return render(request, "index.html")


class UserRegistrationView(CreateView):
    model = CustomUser
    form_class = UserRegistrationForm
    template_name = 'account/user_register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        profile = Profile.objects.create(user=user)
        return super().form_valid(form)


class CustomLoginView(LoginView):
    template_name = 'account/login.html'

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


@login_required
def view_menu_options(request):
    menu_items = Menu.objects.all()
    return render(request, 'main/view_menu_options.html', {'menu_items': menu_items})


@login_required
def add_menu_options(request):
    if request.user.user_type == 'restaurant':
        if not request.user.name:
            return redirect('missing_data_error_restaurant')

        if request.method == 'POST':
            form = MenuForm(request.POST)
            if form.is_valid():
                menu_item = form.save(commit=False)
                menu_item.restaurant = request.user
                menu_item.save()
                return redirect('view_menu_options')
        else:
            initial_data = {'restaurant': request.user, 'quantity': 1}
            form = MenuForm(initial=initial_data)
        return render(request, 'main/add_menu_options.html', {'form': form})
    else:
        return redirect('home')


@login_required
def view_orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'main/view_orders.html', {'orders': orders})


@login_required
def my_listings(request):
    listings = Menu.objects.filter(restaurant=request.user)
    return render(request, 'main/my_listings.html', {'listings': listings})


class MenuOrderView(View):
    def post(self, request, menu_item_id):
        try:
            menu_item = Menu.objects.get(pk=menu_item_id)

            if request.user.user_type == 'user' and not request.user.address:
                return redirect('missing_data_error_user')

            quantity = int(request.POST.get('quantity', 1))

            if quantity <= menu_item.quantity:
                order = Order.objects.create(user=request.user, total_price=menu_item.price * quantity)
                order.menu_items.add(menu_item)

                menu_item.quantity -= quantity
                menu_item.save()

                return redirect('order_confirmation')
            else:
                messages.error(request, 'Not enough available portions for this menu item.')
                return redirect('view_menu_options')

        except Menu.DoesNotExist:
            return redirect('error')


class OrderConfirmationView(TemplateView):
    template_name = 'main/order_confirmation.html'


class RestaurantReviewsView(View):
    template_name = 'main/restaurant_reviews.html'

    def get(self, request, restaurant_id):
        try:
            restaurant = CustomUser.objects.get(pk=restaurant_id, user_type='restaurant')
            reviews = restaurant.restaurant_reviews.all()
            return render(request, self.template_name, {'restaurant': restaurant, 'reviews': reviews})
        except CustomUser.DoesNotExist:
            return redirect('error')

@login_required
def leave_review(request, restaurant_id):
    if request.user.user_type == 'user':
        try:
            restaurant = CustomUser.objects.get(id=restaurant_id, user_type='restaurant')
        except CustomUser.DoesNotExist:
            raise Http404("Restaurant not found")

        if request.method == 'POST':
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.user = request.user
                review.restaurant = restaurant
                review.save()
                messages.success(request, "Your review has been successfully added.")
                return redirect('restaurant_reviews', restaurant_id=restaurant_id)
        else:
            form = ReviewForm()

        context = {'restaurant': restaurant, 'form': form}
        return render(request, 'main/leave_review.html', context)
    else:
        raise Http404("You don't have permission to leave a review.")


class AllOrdersView(View):
    template_name = 'main/all_orders.html'

    def get(self, request):
        orders = Order.objects.all()
        return render(request, self.template_name, {'orders': orders})


class MissingRestaurantNameErrorView(TemplateView):
    template_name = 'errors/missing_data_error.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['error_message'] = "Restaurant name is missing. Please update your profile."
        return context


class MissingUserAddressErrorView(TemplateView):
    template_name = 'errors/missing_data_error.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['error_message'] = "Address is missing. Please update your profile."
        return context


class ErrorView(TemplateView):
    template_name = 'errors/error.html'


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