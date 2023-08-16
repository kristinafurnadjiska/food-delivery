from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .models import Cart, CartItem
from users.models import Profile
from restaurant.models import Restaurant, Meal
from django.db.models import Count
 
class Index(View):
    def get(self, request, *args, **kwargs):
        restaurants = Restaurant.objects.all()

        context = {
            'items': restaurants
        }

        return render(request, 'client/index.html', context)
    
class Preview(View):
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

        if not l.__contains__(meal.restaurant.pk):
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

class CartPreview(View):
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