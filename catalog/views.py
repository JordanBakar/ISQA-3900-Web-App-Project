from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Pizza, Order, OrderDetail, Employee, Member, Guest, Payment


# Homepage
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

    return render(request, 'catalog/index.html', context=context)


# Pizza
class PizzaListView(generic.ListView):
    model = Pizza
    template_name = 'catalog/pizza_list.html'
    context_object_name = 'pizzas'

class PizzaDetailView(generic.DetailView):
    model = Pizza
    template_name = 'catalog/pizza_detail.html'

class PizzaCreateView(LoginRequiredMixin, CreateView):
    model = Pizza
    fields = ['name', 'description', 'price', 'size']
    template_name = 'catalog/pizza_form.html'

class PizzaUpdateView(LoginRequiredMixin, UpdateView):
    model = Pizza
    fields = ['name', 'description', 'price', 'size']
    template_name = 'catalog/pizza_form.html'

class PizzaDeleteView(LoginRequiredMixin, DeleteView):
    model = Pizza
    template_name = 'catalog/pizza_confirm_delete.html'
    success_url = reverse_lazy('pizza_list')


# Order
class OrderListView(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = 'catalog/order_list.html'
    context_object_name = 'orders'

class OrderDetailView(LoginRequiredMixin, generic.DetailView):
    model = Order
    template_name = 'catalog/order_detail.html'

class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    fields = ['member', 'guest', 'employee', 'total_amount', 'order_status']
    template_name = 'catalog/order_form.html'

class OrderUpdateView(LoginRequiredMixin, UpdateView):
    model = Order
    fields = ['member', 'guest', 'employee', 'total_amount', 'order_status']
    template_name = 'catalog/order_form.html'

class OrderDeleteView(LoginRequiredMixin, DeleteView):
    model = Order
    template_name = 'catalog/order_confirm_delete.html'
    success_url = reverse_lazy('order_list')


# Member
class MemberListView(LoginRequiredMixin, generic.ListView):
    model = Member
    template_name = 'catalog/member_list.html'
    context_object_name = 'members'

class MemberDetailView(LoginRequiredMixin, generic.DetailView):
    model = Member
    template_name = 'catalog/member_detail.html'

class MemberCreateView(LoginRequiredMixin, CreateView):
    model = Member
    fields = ['user', 'phone_number', 'street_address', 'city', 'state', 'zip_code']
    template_name = 'catalog/member_form.html'

class MemberUpdateView(LoginRequiredMixin, UpdateView):
    model = Member
    fields = ['user', 'phone_number', 'street_address', 'city', 'state', 'zip_code']
    template_name = 'catalog/member_form.html'

class MemberDeleteView(LoginRequiredMixin, DeleteView):
    model = Member
    template_name = 'catalog/member_confirm_delete.html'
    success_url = reverse_lazy('member_list')


# Cart
class ShoppingCartView(generic.TemplateView):
    template_name = 'catalog/cart.html'

def add_to_cart(request, pizza_id):
    """Add a pizza to the shopping cart stored in the session."""
    cart = request.session.get('cart', {})
    cart[pizza_id] = cart.get(pizza_id, 0) + 1
    request.session['cart'] = cart
    messages.success(request, "Pizza added to cart!")
    return redirect('cart')

def remove_from_cart(request, pizza_id):
    """Remove a pizza from the shopping cart stored in the session."""
    cart = request.session.get('cart', {})
    if pizza_id in cart:
        del cart[pizza_id]
        request.session['cart'] = cart
        messages.success(request, "Pizza removed from cart.")
    return redirect('cart')


# Static
class AboutView(generic.TemplateView):
    template_name = 'catalog/about.html'
