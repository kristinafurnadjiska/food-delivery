from django.contrib import admin
from .models import Meal, Order, Category, Restaurant

# Register your models here.
admin.site.register(Meal)
admin.site.register(Order)
admin.site.register(Category)
admin.site.register(Restaurant)