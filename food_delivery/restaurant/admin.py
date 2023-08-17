from django.contrib import admin
from .models import Meal, Order, Category, Restaurant, OrderItem

# Register your models here.
admin.site.register(Meal)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Category)
admin.site.register(Restaurant)