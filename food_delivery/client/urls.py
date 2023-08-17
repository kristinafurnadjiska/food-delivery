from django.urls import path
from client.views import Index, Preview, CartPreview, OrderCreateView, OrderConfirmation

urlpatterns = [
    path('', Index.as_view(), name='client-index'),
    path('cart', CartPreview.as_view(), name='client-cart'),
    path('checkout', OrderCreateView.as_view(), name='client-checkout'),
    path('confirmation', OrderConfirmation.as_view(), name='client-confirmation'),
    path('<int:pk>/preview', Preview.as_view(), name='client-restaurant-preview')
]