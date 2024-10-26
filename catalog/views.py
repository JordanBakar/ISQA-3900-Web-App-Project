from .models import Pizza, Order, OrderDetail, Employee, Member, Guest, Payment
from django.shortcuts import render, get_list_or_404
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.contrib import messages
from django.shortcuts import redirect




def index(request):
    """View function for home page of the site."""
    num_pizzas = Pizza.objects.all().count()
    num_orders = Order.objects.all().count()
    num_employees = Employee.objects.count()
    num_members = Member.objects.count()

    context = {
        'num_pizzas': num_pizzas,
        'num_orders': num_orders,
        'num_employees': num_employees,
        'num_members': num_members,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'catalog/index.html', context=context)


def pizza_list(request):
    """View function to display a list of pizzas."""
    pizzas = Pizza.objects.all()

    context = {
        'pizzas': pizzas,
    }

    return render(request, 'pizza_list.html', context=context)


def order_list(request):
    """View function to display a list of orders."""
    orders = Order.objects.all()

    context = {
        'orders': orders,
    }

    return render(request, 'catalog/order_list.html', context=context)


def order_detail(request, order_id):
    """View function to display the details of a specific order."""
    order = Order.objects.get(id=order_id)
    order_details = OrderDetail.objects.filter(order=order)

    context = {
        'order': order,
        'order_details': order_details,
    }

    return render(request, 'order_detail.html', context=context)

class OrderListView(LoginRequiredMixin, generic.ListView):
    model = Order

class AboutView(generic.ListView):
    model = Payment

class ShoppingCartView(generic.ListView):
    model = Payment