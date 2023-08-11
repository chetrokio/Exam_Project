from django.test import TestCase, Client

from .forms import UserRegistrationForm, CustomUserProfileForm, MenuForm, OrderForm, ReviewForm
from .models import CustomUser, Menu, Order, Review

###MODEL TEST###
class CustomUserModelTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            email='user@example.com',
            username='testuser',
            name='Test User',
            phone_number='1234567890',
            address='123 Main St',
            password='testpass',
            user_type='user'
        )

    def test_create_user(self):
        self.assertEqual(self.user.email, 'user@example.com')
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.name, 'Test User')
        self.assertEqual(self.user.phone_number, '1234567890')
        self.assertEqual(self.user.address, '123 Main St')
        self.assertEqual(self.user.user_type, 'user')
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)

class MenuModelTestCase(TestCase):
    def setUp(self):
        self.restaurant = CustomUser.objects.create(
            email='restaurant@example.com',
            username='testrestaurant',
            name='Test Restaurant',
            phone_number='9876543210',
            address='456 Restaurant St',
            password='testpass',
            user_type='restaurant'
        )
        self.menu_item = Menu.objects.create(
            restaurant=self.restaurant,
            dish_name='Test Dish',
            description='This is a test dish.',
            price=10.99,
            quantity=5
        )

    def test_create_menu_item(self):
        self.assertEqual(self.menu_item.restaurant, self.restaurant)
        self.assertEqual(self.menu_item.dish_name, 'Test Dish')
        self.assertEqual(self.menu_item.description, 'This is a test dish.')
        self.assertEqual(self.menu_item.price, 10.99)
        self.assertEqual(self.menu_item.quantity, 5)


class OrderModelTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            email='user@example.com',
            username='testuser',
            name='Test User',
            phone_number='1234567890',
            address='123 Main St',
            password='testpass',
            user_type='user'
        )
        self.restaurant = CustomUser.objects.create(
            email='restaurant@example.com',
            username='testrestaurant',
            name='Test Restaurant',
            phone_number='9876543210',
            address='456 Restaurant St',
            password='testpass',
            user_type='restaurant'
        )
        self.menu_item = Menu.objects.create(
            restaurant=self.restaurant,
            dish_name='Test Dish',
            description='This is a test dish.',
            price=10.99,
            quantity=5
        )
        self.order = Order.objects.create(
            user=self.user,
            restaurant=self.restaurant,
            order_status='pending',
            total_price=10.99
        )
        self.order.menu_items.add(self.menu_item)

    def test_create_order(self):
        self.assertEqual(self.order.user, self.user)
        self.assertEqual(self.order.restaurant, self.restaurant)
        self.assertEqual(self.order.order_status, 'pending')
        self.assertEqual(self.order.total_price, 10.99)
        self.assertTrue(self.menu_item in self.order.menu_items.all())

    # Additional test cases
    def test_order_str(self):
        self.assertEqual(str(self.order), f"Order #{self.order.pk} - User: {self.user.username}")

###FORM TEST###
class FormsTestCase(TestCase):

    def test_user_registration_form(self):
        form_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'user_type': 'user',
        }
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_custom_user_profile_form(self):
        user = CustomUser.objects.create(email='test@example.com', username='testuser', user_type='user')
        form_data = {
            'username': 'updateduser',
            'email': 'updated@example.com',
            'user_type': 'user',
            'name': 'John Doe',
            'phone_number': '1234567890',
            'address': '123 Main St',
        }
        form = CustomUserProfileForm(data=form_data, instance=user)
        self.assertTrue(form.is_valid())


    def test_order_form(self):
        user = CustomUser.objects.create(email='test@example.com', username='testuser', user_type='user')
        restaurant = CustomUser.objects.create(email='restaurant@example.com', username='restaurantuser', user_type='restaurant')
        menu_item = Menu.objects.create(restaurant=restaurant, dish_name='Test Dish', quantity=10, description='Test description', price=9.99)
        form_data = {
            f'quantity_{menu_item.pk}': 5,
        }
        form = OrderForm(menu_items=[menu_item], data=form_data)
        self.assertTrue(form.is_valid())

    def test_review_form(self):
        user = CustomUser.objects.create(email='test@example.com', username='testuser', user_type='user')
        restaurant = CustomUser.objects.create(email='restaurant@example.com', username='restaurantuser', user_type='restaurant')
        form_data = {
            'rating': 5,
            'comment': 'Great food!',
        }
        form = ReviewForm(data=form_data)
        self.assertTrue(form.is_valid())

