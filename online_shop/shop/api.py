from django.urls import path
from .views import ProductList, ProductDetail, CartDetail

urlpatterns = [
    path('products/', ProductList.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetail.as_view(), name='product-detail'),
    path('cart/', CartDetail.as_view(), name='cart-detail'),
]
