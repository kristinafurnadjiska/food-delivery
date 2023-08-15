from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth import views as auth_views

from .forms import UserRegistrationForm
from .models import Profile

class Register(View):
  def get(self, request, *args, **kwargs): 
    form = UserRegistrationForm()
  
    context = { 
      'form': form 
    } 

    return render(request, 'users/register.html', context)
  
  def post(self, request):
    form = UserRegistrationForm(request.POST)

    if form.is_valid():
      user = form.save()

      data = form.cleaned_data
      Profile.objects.create(user=user, type=data['type'], address=data['address'])

      return redirect('login')
    
    context = { 
      'form': form 
    } 

    return render(request, 'users/register.html', context)


class Login(auth_views.LoginView):
  template_name = 'users/login.html'

  def get_success_url(self) -> str:
    profile = Profile.objects.get(user=self.request.user.pk)
    if profile.is_owner():
      return '/restaurants/home'
    if profile.is_regular_user():
      return '/order'
    return super().get_success_url()