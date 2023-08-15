from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    USER_CHOICES = [
        ("owner", "Owner"),
        ("user", "User"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=100, choices=USER_CHOICES)
    address = models.CharField(max_length=200)

    def is_owner(self):
        return self.type == 'owner'

    def is_regular_user(self):
        return self.type == 'user'

    def __str__(self):
        return f'{self.user.username} Profile'