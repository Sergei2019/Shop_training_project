from django.urls import path
from .views import register, product_list, add_to_cart, view_cart


urlpatterns = [
    path('register/', register, name='register'),
    path('', product_list, name='product_list'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='view_cart'),
]

