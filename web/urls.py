from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .views import UserRegistrationView, CustomLogoutView, \
    CustomLoginView, index, WikipediaStatisticsView, add_menu_options, view_menu_options, \
    OrderConfirmationView, ErrorView, MenuOrderView

urlpatterns = [
    path("", index, name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', UserRegistrationView.as_view(), name='user_registration'),
    path('add-menu-option/', add_menu_options, name='add_menu_option'),
    path('view-menu-options/', view_menu_options, name='view_menu_options'),
    path("leftovers-info/", WikipediaStatisticsView, name='leftovers-info'),
    path('order/confirmation/', OrderConfirmationView.as_view(), name='order_confirmation'),
    path('error/', ErrorView.as_view(), name='error'),
    path('order/<int:menu_item_id>/', MenuOrderView.as_view(), name='order_menu_item'),


]