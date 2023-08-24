from django.db import models
from users.models import Profile

# Create your models here.
class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    address = models.CharField(max_length=100)
    image = models.ImageField(upload_to='restaurants/', default='default_restaurant.png')
    owner = models.OneToOneField(Profile, related_name='owner', on_delete=models.CASCADE)

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name 
    
class Meal(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to = 'meals/')
    price = models.IntegerField()
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, related_name='category')

    def __str__(self) -> str:
        return self.name
    
class Order(models.Model):
    PAY_CHOICES = [
        ('cash', 'Pay with cash'),
        ('card', 'Pay with card')
    ]

    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('In progress', 'In progress'),
        ('Delivering', 'Delivering'),
        ('Delivered', 'Delivered'),
    ]

    created_on = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=100, choices=PAY_CHOICES)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='Active')
    price = models.IntegerField()
    address = models.CharField(max_length=100)
    is_paid = models.BooleanField(default=False)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def __str__(self):
        return f'Order: {self.created_on.strftime("%b %d %I: %M %p")}'
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    quantity = models.IntegerField()