from django.urls import path
from .views import Index, RestaurantCreateView,  Setup,  RestaurantPreview, RestaurantUpdateView

urlpatterns = [
  path('home/', Index.as_view(), name = 'restaurant-home'),
  path('setup/', Setup.as_view(), name='restaurant-setup'),
  path('preview/', RestaurantPreview.as_view(), name='restaurant-preview'),
  path('edit/', RestaurantUpdateView.as_view(), name='restaurant-edit'),
  path('create/', RestaurantCreateView.as_view(), name='restaurant-create')
]