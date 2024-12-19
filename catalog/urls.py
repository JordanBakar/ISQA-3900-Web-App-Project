from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    # Homepage
    path('', views.index, name='index'),  # Main homepage

    # Order URLs
    path('orders/', views.OrderListView.as_view(), name='order_list'),  # List all orders
    path('order/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),  # View details of a specific order
    path('order/create/', views.OrderCreateView.as_view(), name='order_create'),  # Create a new order
    path('order/<int:pk>/update/', views.OrderUpdateView.as_view(), name='order_update'),  # Update an existing order
    path('order/<int:pk>/delete/', views.OrderDeleteView.as_view(), name='order_delete'),  # Delete an order

    # Pizza URLs
    path('pizzas/', views.PizzaListView.as_view(), name='pizza_list'),  # List all pizzas
    path('pizza/<int:pk>/', views.PizzaDetailView.as_view(), name='pizza_detail'),  # View details of a specific pizza
    path('pizza/create/', views.PizzaCreateView.as_view(), name='pizza_create'),  # Create a new pizza
    path('pizza/<int:pk>/update/', views.PizzaUpdateView.as_view(), name='pizza_update'),  # Update an existing pizza
    path('pizza/<int:pk>/delete/', views.PizzaDeleteView.as_view(), name='pizza_delete'),  # Delete a pizza

    # Member URLs
    path('members/', views.MemberListView.as_view(), name='member_list'),  # List all members
    path('member/<int:pk>/', views.MemberDetailView.as_view(), name='member_detail'),  # View details of a specific member
    path('member/create/', views.MemberCreateView.as_view(), name='member_create'),  # Create a new member
    path('member/<int:pk>/update/', views.MemberUpdateView.as_view(), name='member_update'),  # Update an existing member
    path('member/<int:pk>/delete/', views.MemberDeleteView.as_view(), name='member_delete'),  # Delete a member

    # Cart URLs
    path('cart/', views.cart_view, name='cart'),  # View the cart contents
    path('cart/add/<int:pizza_id>/', views.add_to_cart, name='add_to_cart'),  # Add a pizza to the cart
    path('cart/remove/<int:pizza_id>/', views.remove_from_cart, name='remove_from_cart'),  # Remove or decrement a pizza from the cart

    # Payment URL
    path('payment/', views.payment_view, name='payment'),  # Display the payment page
    path('payment/process/', views.process_payment, name='process_payment'),

    # Static URLs
    path('about/', TemplateView.as_view(template_name='catalog/about.html'), name='about'),  # Static About page
]
