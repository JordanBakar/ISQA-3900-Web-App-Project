from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.index, name='index'),
    path('order_list/', views.OrderListView.as_view(), name='order_list'),
    path('shopping_cart/', views.ShoppingCartView.as_view(), name='shopping_cart'),
    path('about/', TemplateView.as_view(template_name='catalog/about.html'), name='about'),
]