from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .models import Cart, CartItem
from users.models import Profile
from restaurant.models import Restaurant, Meal, Order, OrderItem
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView

class Index(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        profile = Profile.objects.get(user=self.request.user.pk)
        return profile.is_regular_user()

    def get(self, request, *args, **kwargs):
        restaurants = Restaurant.objects.all()

        context = {
            'items': restaurants
        }

        return render(request, 'client/index.html', context)
    
class Preview(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        profile = Profile.objects.get(user=self.request.user.pk)
        return profile.is_regular_user()
    
    def get(self, request, *args, **kwargs):
        id = kwargs['pk']

        try:
            restaurant = Restaurant.objects.get(id=id)
        except:
            return redirect('client-index')

        # get every item for each category
        drinks = Meal.objects.filter(category__name__contains="Drinks", restaurant__exact=restaurant)
        desserts = Meal.objects.filter(category__name__contains="Desserts", restaurant__exact=restaurant)
        breakfast = Meal.objects.filter(category__name__contains="Breakfast", restaurant__exact=restaurant)
        lunch = Meal.objects.filter(category__name__contains="Lunch", restaurant__exact=restaurant)
        dinner = Meal.objects.filter(category__name__contains="Dinner", restaurant__exact=restaurant)

        # pass into context
        context = {
            'drinks': drinks,
            'desserts': desserts,
            'breakfast': breakfast,
            'lunch': lunch,
            'dinner': dinner,
            'restaurant': restaurant
        }

        # return template
        return render(request, 'client/restaurant.html', context)
    
    def post(self, request, *args, **kwargs):
        id = kwargs['pk']
        data = self.request.POST.dict()
        item_id = data['item_id']
        item_value = int(data['item_value'])

        owner = Profile.objects.get(user=self.request.user.pk)
        meal = Meal.objects.get(pk=item_id);
        restaurant = meal.restaurant;

        cart = Cart.objects.get(owner=owner)
        query = CartItem.objects.values_list('restaurant__pk', flat=True)
        l = list(query)

        if len(l) > 0 and not l.__contains__(meal.restaurant.pk):
            messages.info(request, 'Cannot add to current cart from different restaurant!')

            return redirect('client-restaurant-preview', pk=id)

        try:
            cart_item = CartItem.objects.get(cart=cart, restaurant=restaurant, meal=meal)
        except:
            cart_item = CartItem.objects.create(cart=cart, meal=meal, restaurant=restaurant, quantity=0)

        cart_item.quantity = cart_item.quantity + item_value;
        cart_item.save()
        
        messages.success(request,'Successfully added to cart')

        return redirect('client-restaurant-preview', pk=id)

class CartPreview(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        profile = Profile.objects.get(user=self.request.user.pk)
        return profile.is_regular_user()

    def get(self, request):
        owner = Profile.objects.get(user=self.request.user.pk)  
        cart = Cart.objects.get(owner=owner)

        items = CartItem.objects.filter(cart=cart).all()

        total = sum([item.meal.price * item.quantity for item in items])

        context = {
            'items': items,
            'total': total
        }

        return render(request, 'client/cart.html', context)
    
    def post(self, request):
        data = self.request.POST.dict()
        item_id = data['item_id']
        action = data['action']

        if action == 'remove':
            owner = Profile.objects.get(user=self.request.user.pk)  
            cart = Cart.objects.get(owner=owner)
            meal = Meal.objects.get(pk=item_id);

            cart_item = CartItem.objects.get(cart=cart, meal=meal)
            cart_item.delete()

        messages.success(request,'Successfully removed to cart')

        return redirect('client-cart')

class OrderCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    success_url = ''
    model = Order
    template_name = 'client/checkout_form.html'
    fields = ['address', 'method']

    def test_func(self):
        profile = Profile.objects.get(user=self.request.user.pk)
        return profile.is_regular_user()

    def get(self, request, *args, **kwargs):
        owner = Profile.objects.get(user=self.request.user.pk)
        self.initial['address'] = owner.address
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if not form.is_valid():
            return self.form_invalid(form)

        owner = Profile.objects.get(user=self.request.user.pk)
        cart = Cart.objects.get(owner=owner)
        items = CartItem.objects.filter(cart=cart).all()
        price = sum([item.meal.price * item.quantity for item in items])
    
        data = self.request.POST.dict()
        address = data['address']
        method = data['method']
        is_paid = method == 'card';

        order = Order.objects.create(method=method, price=price, address=address, is_paid=is_paid)
        for item in items:
            OrderItem.objects.create(order=order, meal=item.meal, quantity=item.quantity)
            item.delete()

        return redirect('client-confirmation')

class OrderConfirmation(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        profile = Profile.objects.get(user=self.request.user.pk)
        return profile.is_regular_user()
    
    def get(self, request):
        return render(request, 'client/confirmation.html')