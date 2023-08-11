from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views as v

urlpatterns = [
    path("", v.index, name='home'),
    path("leftovers-info/", v.WikipediaStatisticsView, name='leftovers-info'),

    path('login/', v.CustomLoginView.as_view(), name='login'),
    path('logout/', v.CustomLogoutView.as_view(), name='logout'),
    path('register/', v.UserRegistrationView.as_view(), name='user_registration'),

    path('add-menu-option/', v.add_menu_options, name='add_menu_option'),
    path('all-orders/', v.AllOrdersView.as_view(), name='all_orders'),
    path('my-listings/', v.my_listings, name='my_listings'),
    path('view-orders/', v.view_orders, name='view_orders'),
    path('view-menu-options/', v.view_menu_options, name='view_menu_options'),

    path('order/confirmation/', v.OrderConfirmationView.as_view(), name='order_confirmation'),
    path('order/<int:menu_item_id>/', v.MenuOrderView.as_view(), name='order_menu_item'),

    path('restaurant-reviews/<int:restaurant_id>/', v.RestaurantReviewsView.as_view(), name='restaurant_reviews'),
    path('leave-review/<int:restaurant_id>/', v.leave_review, name='leave_review'),

    path('missing_data_error/restaurant/',
         v.MissingRestaurantNameErrorView.as_view(), name='missing_data_error_restaurant'),
    path('missing_data_error/user/', v.MissingUserAddressErrorView.as_view(), name='missing_data_error_user'),
    path('error/', v.ErrorView.as_view(), name='error'),


]