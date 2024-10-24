from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('order_list/', views.OrderListView.as_view(), name='order_list'),
    path('shopping_cart/', views.ShoppingCartView.as_view(), name='shopping_cart'),
]