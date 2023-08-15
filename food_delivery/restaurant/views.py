from typing import Any, Optional
from django.db import models
from django.shortcuts import render, redirect
from django.views import View
from .models import Restaurant, Meal
from users.models import Profile
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

class Index(View):
    def get(self, request):
        owner = Profile.objects.get(user=self.request.user.pk)

        try:
            restaurant = Restaurant.objects.get(owner=owner)
        except Restaurant.DoesNotExist:
            return redirect('restaurant-setup')

        context = {
            'object': restaurant
        }

        return render(request, 'restaurant/restaurant_detail.html', context)
    
class Setup(View):
    def get(self, request):
        return render(request, 'restaurant/setup.html')
    
class RestaurantPreview(View):
    def get(self, request):
        owner = Profile.objects.get(user=self.request.user.pk)
        restaurant = Restaurant.objects.get(owner=owner.pk)
        items = Meal.objects.filter(restaurant=restaurant)

        context = {
            'items': items.all()
        }
        return render(request, 'restaurant/preview.html', context)
    
class RestaurantCreateView(LoginRequiredMixin, CreateView):
    success_url = '/restaurants/home'
    model = Restaurant
    fields = ['name', 'description', 'address', 'image']

    def form_valid(self, form):
        owner = Profile.objects.get(user=self.request.user.pk)
        form.instance.owner = owner
        return super().form_valid(form)
    
class RestaurantUpdateView(LoginRequiredMixin, UpdateView):
    success_url = '/restaurants/home'
    model = Restaurant
    fields = ['name', 'description', 'address', 'image']

    def get_object(self):
        owner = Profile.objects.get(user=self.request.user.pk)
        restaurant = Restaurant.objects.get(owner=owner.pk)
        return restaurant
