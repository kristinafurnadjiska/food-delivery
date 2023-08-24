from django.shortcuts import render, redirect
from django.views import View
from .models import Restaurant, Meal, Order, OrderItem
from users.models import Profile
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, DeleteView

class Index(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        profile = Profile.objects.get(user=self.request.user.pk)
        return profile.is_owner()

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
    
class Setup(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        profile = Profile.objects.get(user=self.request.user.pk)
        return profile.is_owner()
    
    def get(self, request):
        return render(request, 'restaurant/setup.html')
    
class RestaurantPreview(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        profile = Profile.objects.get(user=self.request.user.pk)
        return profile.is_owner()
    
    def get(self, request):
        owner = Profile.objects.get(user=self.request.user.pk)
        try:
            restaurant = Restaurant.objects.get(owner=owner)
        except Restaurant.DoesNotExist:
            return redirect('restaurant-setup')
        items = Meal.objects.filter(restaurant=restaurant)

        context = {
            'items': items.all()
        }
        return render(request, 'restaurant/preview.html', context)
    
class RestaurantCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    success_url = '/restaurants/home'
    model = Restaurant
    fields = ['name', 'description', 'address', 'image']

    def test_func(self):
        profile = Profile.objects.get(user=self.request.user.pk)
        return profile.is_owner()

    def form_valid(self, form):
        owner = Profile.objects.get(user=self.request.user.pk)
        form.instance.owner = owner
        return super().form_valid(form)
    
class RestaurantUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    success_url = '/restaurants/home'
    model = Restaurant
    fields = ['name', 'description', 'address', 'image']

    def test_func(self):
        profile = Profile.objects.get(user=self.request.user.pk)
        return profile.is_owner()

    def get_object(self):
        owner = Profile.objects.get(user=self.request.user.pk)
        restaurant = Restaurant.objects.get(owner=owner.pk)
        return restaurant

class MealCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    success_url = '/restaurants/preview'
    template_name = 'meals/meal_form.html'
    model = Meal
    fields = ['name', 'description', 'image', 'price', 'category']

    def test_func(self):
        profile = Profile.objects.get(user=self.request.user.pk)
        return profile.is_owner()

    def form_valid(self, form):
        owner = Profile.objects.get(user=self.request.user.pk)
        restaurant = Restaurant.objects.get(owner = owner.pk);
        form.instance.restaurant = restaurant
        return super().form_valid(form)

class MealEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    success_url = '/restaurants/preview'
    model = Meal
    template_name = 'meals/meal_form.html'
    fields = ['name', 'description', 'price', 'image', 'category']

    def test_func(self):
        profile = Profile.objects.get(user=self.request.user.pk)
        return profile.is_owner()

class MealDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Meal
    template_name = 'meals/meal_confirm_delete.html'
    success_url = '/restaurants/preview'

    def test_func(self):
        profile = Profile.objects.get(user=self.request.user.pk)
        return profile.is_owner()

class OrdersPreview(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        profile = Profile.objects.get(user=self.request.user.pk)
        return profile.is_owner()

    def get(self, request):
        owner = Profile.objects.get(user=self.request.user.pk)
        try:
            restaurant = Restaurant.objects.get(owner=owner)
        except Restaurant.DoesNotExist:
            return redirect('restaurant-setup')
        
        orders = Order.objects.filter(restaurant=restaurant)

        context = {
            'items': orders
        }

        return render(request, 'orders/index.html', context)
    
class OrderPreview(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    success_url = '/restaurants/orders'
    model = Order
    template_name = 'orders/preview.html'
    fields = ['status']

    def test_func(self):
        profile = Profile.objects.get(user=self.request.user.pk)
        return profile.is_owner()
    
    def get_context_data(self, **kwargs):
        id = int(self.request.path.split('/')[-1])
        order = Order.objects.get(pk=id)

        context = super().get_context_data(**kwargs)

        meals = OrderItem.objects.filter(order=order);

        context['item'] = order
        context['meals'] = meals

        return context