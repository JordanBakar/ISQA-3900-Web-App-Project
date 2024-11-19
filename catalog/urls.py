from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    # Homepage
    path('', views.index, name='index'),  # Main homepage, renders index.html

    # Order
    path('orders/', views.OrderListView.as_view(template_name='catalog/order_list.html'), name='order_list'),  # List all orders
    path('order/<int:pk>/', views.OrderDetailView.as_view(template_name='catalog/order_detail.html'), name='order_detail'),  # View a specific order by ID
    path('order/create/', views.OrderCreateView.as_view(template_name='catalog/order_form.html'), name='order_create'),  # Form to create a new order
    path('order/<int:pk>/update/', views.OrderUpdateView.as_view(template_name='catalog/order_form.html'), name='order_update'),  # Form to update an existing order
    path('order/<int:pk>/delete/', views.OrderDeleteView.as_view(), name='order_delete'),  # Delete an order by ID

    # Pizza
    path('pizzas/', views.PizzaListView.as_view(template_name='catalog/pizza_list.html'), name='pizza_list'),  # List all pizzas
    path('pizza/<int:pk>/', views.PizzaDetailView.as_view(template_name='catalog/pizza_detail.html'), name='pizza_detail'),  # View details of a specific pizza by ID
    path('pizza/create/', views.PizzaCreateView.as_view(template_name='catalog/pizza_form.html'), name='pizza_create'),  # Form to create a new pizza
    path('pizza/<int:pk>/update/', views.PizzaUpdateView.as_view(template_name='catalog/pizza_form.html'), name='pizza_update'),  # Form to update an existing pizza
    path('pizza/<int:pk>/delete/', views.PizzaDeleteView.as_view(), name='pizza_delete'),  # Delete a pizza by ID

    # Member
    path('members/', views.MemberListView.as_view(template_name='catalog/member_list.html'), name='member_list'),  # List all members
    path('member/<int:pk>/', views.MemberDetailView.as_view(template_name='catalog/member_detail.html'), name='member_detail'),  # View details of a specific member by ID
    path('member/create/', views.MemberCreateView.as_view(template_name='catalog/member_form.html'), name='member_create'),  # Form to create a new member
    path('member/<int:pk>/update/', views.MemberUpdateView.as_view(template_name='catalog/member_form.html'), name='member_update'),  # Form to update an existing member
    path('member/<int:pk>/delete/', views.MemberDeleteView.as_view(), name='member_delete'),  # Delete a member by ID

    # Cart
    path('cart/', views.ShoppingCartView.as_view(template_name='catalog/cart.html'), name='cart'),  # View cart contents
    path('cart/add/<int:pizza_id>/', views.add_to_cart, name='add_to_cart'),  # Add a pizza to the cart by pizza ID
    path('cart/remove/<int:pizza_id>/', views.remove_from_cart, name='remove_from_cart'),  # Remove a pizza from the cart by pizza ID

    # Static
    path('about/', TemplateView.as_view(template_name='catalog/about.html'), name='about'),  # Static About page

    #Order_List
    path('menu/', views.order_list, name='order_list'),
]
