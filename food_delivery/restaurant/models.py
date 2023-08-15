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
    created_on = models.DateTimeField(auto_now_add=True)
    price = models.IntegerField()
    items = models.ManyToManyField(Meal, related_name='items', blank=True)

    def __str__(self):
        return f'Order: {self.created_on.strftime("%b %d %I: %M %p")}'