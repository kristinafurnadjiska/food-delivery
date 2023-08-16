from django.urls import path
from client.views import Index, Preview, CartPreview

urlpatterns = [
    path('', Index.as_view(), name='client-index'),
    path('cart', CartPreview.as_view(), name='client-cart'),
    path('<int:pk>/preview', Preview.as_view(), name='client-restaurant-preview')
]