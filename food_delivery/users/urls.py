from django.urls import path
from .views import Register, Login, Landing
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', Register.as_view(), name='register'),
    path('landing/', Landing.as_view(), name='landing'),
    path('login/', Login.as_view(), name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name = 'logout'),
]