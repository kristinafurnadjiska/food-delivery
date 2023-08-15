from django.urls import path
from .views import Index, RestaurantCreateView,  Setup,  RestaurantPreview, RestaurantUpdateView, MealCreateView, MealEditView, MealDeleteView

urlpatterns = [
  path('home/', Index.as_view(), name = 'restaurant-home'),
  path('setup/', Setup.as_view(), name='restaurant-setup'),
  path('preview/', RestaurantPreview.as_view(), name='restaurant-preview'),
  path('edit/', RestaurantUpdateView.as_view(), name='restaurant-edit'),
  path('create/', RestaurantCreateView.as_view(), name='restaurant-create'),
  path('meals/create', MealCreateView.as_view(), name='meals-create'),
  path('meals/<int:pk>/edit', MealEditView.as_view(), name='meals-update'),
  path('meals/<int:pk>/delete', MealDeleteView.as_view(), name='meals-delete'),
]