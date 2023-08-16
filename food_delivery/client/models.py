from django.db import models
from users.models import Profile
from restaurant.models import Meal, Restaurant

class Cart(models.Model):
    owner = models.OneToOneField(Profile, on_delete=models.CASCADE)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    quantity = models.IntegerField()