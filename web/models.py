from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from web.manager import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    USER_TYPE_CHOICES = (
        ('user', 'User'),
        ('restaurant', 'Restaurant'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='user')

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'name', 'phone_number', 'address']
    objects = CustomUserManager()

    def __str__(self):
        return self.name


class Menu(models.Model):
    restaurant = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'user_type': 'restaurant'})
    dish_name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(CustomUser,
                             on_delete=models.CASCADE,
                             related_name='user_orders',
                             limit_choices_to={'user_type': 'user'})
    restaurant = models.ForeignKey(CustomUser,
                                   on_delete=models.CASCADE,
                                   related_name='restaurant_orders',
                                   limit_choices_to={'user_type': 'restaurant'})
    menu_items = models.ManyToManyField(Menu)
    order_status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed')])
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order #{self.pk} - User: {self.user.username}"


class Review(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': 'user'},
        related_name='user_reviews',
    )
    restaurant = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': 'restaurant'},
        related_name='restaurant_reviews',
    )
    rating = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    comment = models.TextField()

    def __str__(self):
        return f"Review #{self.pk} - User: {self.user.username}"

