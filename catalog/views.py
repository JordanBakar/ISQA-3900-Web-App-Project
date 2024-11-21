from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Pizza, Order, OrderDetail, Employee, Member, Guest


# Homepage
def index(request):
    """View function for the homepage of the site."""
    # Fetch counts for display on the homepage
    context = {
        'num_pizzas': Pizza.objects.count(),
        'num_orders': Order.objects.count(),
        'num_employees': Employee.objects.count(),
        'num_members': Member.objects.count(),
    }
    return render(request, 'catalog/index.html', context=context)


# Pizza Views
class PizzaListView(generic.ListView):
    """Displays a list of all pizzas."""
    model = Pizza
    template_name = 'catalog/pizza_list.html'
    context_object_name = 'pizzas'


class PizzaDetailView(generic.DetailView):
    """Displays detailed information about a single pizza."""
    model = Pizza
    template_name = 'catalog/pizza_detail.html'


class PizzaCreateView(LoginRequiredMixin, CreateView):
    """Allows creation of a new pizza."""
    model = Pizza
    fields = ['name', 'description', 'price']
    template_name = 'catalog/pizza_form.html'


class PizzaUpdateView(LoginRequiredMixin, UpdateView):
    """Allows editing an existing pizza."""
    model = Pizza
    fields = ['name', 'description', 'price']
    template_name = 'catalog/pizza_form.html'


class PizzaDeleteView(LoginRequiredMixin, DeleteView):
    """Allows deletion of a pizza."""
    model = Pizza
    template_name = 'catalog/pizza_confirm_delete.html'
    success_url = reverse_lazy('pizza_list')


# Order Views
class OrderListView(LoginRequiredMixin, generic.ListView):
    """Displays a list of all orders."""
    model = Order
    template_name = 'catalog/order_list.html'
    context_object_name = 'orders'


class OrderDetailView(LoginRequiredMixin, generic.DetailView):
    """Displays detailed information about a specific order."""
    model = Order
    template_name = 'catalog/order_detail.html'


class OrderCreateView(LoginRequiredMixin, CreateView):
    """Allows creation of a new order."""
    model = Order
    fields = ['member', 'guest', 'employee', 'total_amount', 'order_status']
    template_name = 'catalog/order_form.html'


class OrderUpdateView(LoginRequiredMixin, UpdateView):
    """Allows updating an existing order."""
    model = Order
    fields = ['member', 'guest', 'employee', 'total_amount', 'order_status']
    template_name = 'catalog/order_form.html'


class OrderDeleteView(LoginRequiredMixin, DeleteView):
    """Allows deletion of an order."""
    model = Order
    template_name = 'catalog/order_confirm_delete.html'
    success_url = reverse_lazy('order_list')


# Member Views
class MemberListView(LoginRequiredMixin, generic.ListView):
    """Displays a list of all members."""
    model = Member
    template_name = 'catalog/member_list.html'
    context_object_name = 'members'


class MemberDetailView(LoginRequiredMixin, generic.DetailView):
    """Displays detailed information about a specific member."""
    model = Member
    template_name = 'catalog/member_detail.html'


class MemberCreateView(LoginRequiredMixin, CreateView):
    """Allows creation of a new member."""
    model = Member
    fields = ['user', 'phone_number', 'street_address', 'city', 'state', 'zip_code']
    template_name = 'catalog/member_form.html'


class MemberUpdateView(LoginRequiredMixin, UpdateView):
    """Allows updating an existing member."""
    model = Member
    fields = ['user', 'phone_number', 'street_address', 'city', 'state', 'zip_code']
    template_name = 'catalog/member_form.html'


class MemberDeleteView(LoginRequiredMixin, DeleteView):
    """Allows deletion of a member."""
    model = Member
    template_name = 'catalog/member_confirm_delete.html'
    success_url = reverse_lazy('member_list')


# Cart Views
def cart_view(request):
    """Displays the shopping cart with all items."""
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for pizza_id, quantity in cart.items():
        try:
            pizza = Pizza.objects.get(pizza_id=pizza_id)  # Use 'pizza_id' here
            cart_items.append({
                'pizza': pizza,
                'quantity': quantity,
                'subtotal': pizza.price * quantity
            })
            total += pizza.price * quantity
        except Pizza.DoesNotExist:
            continue  # Skip invalid items

    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'catalog/cart.html', context)



def add_to_cart(request, pizza_id):
    """Adds a pizza to the shopping cart stored in the session."""
    try:
        # Use pizza_id to query the Pizza model
        pizza = Pizza.objects.get(pizza_id=pizza_id)
        cart = request.session.get('cart', {})
        cart[str(pizza_id)] = cart.get(str(pizza_id), 0) + 1
        request.session['cart'] = cart
        messages.success(request, f"{pizza.name} added to cart!")
    except Pizza.DoesNotExist:
        messages.error(request, "Invalid pizza ID.")
    return redirect('cart')


def remove_from_cart(request, pizza_id):
    """Decrements the quantity of a pizza in the shopping cart stored in the session."""
    try:
        pizza = Pizza.objects.get(pizza_id=pizza_id)
        cart = request.session.get('cart', {})

        if str(pizza_id) in cart:
            if cart[str(pizza_id)] > 1:
                cart[str(pizza_id)] -= 1  # Decrements the quantity
                messages.success(request, f"One {pizza.name} removed from cart.")
            else:
                del cart[str(pizza_id)]  # Remove the pizza if quantity reaches zero
                messages.success(request, f"{pizza.name} removed from cart.")

            request.session['cart'] = cart  # Save the updated cart to the session
        else:
            messages.error(request, f"{pizza.name} is not in the cart.")
    except Pizza.DoesNotExist:
        messages.error(request, "Invalid pizza ID.")

    return redirect('cart')


# Static Pages
class AboutView(generic.TemplateView):
    """Displays the about page."""
    template_name = 'catalog/about.html'


# Order List Function
def order_list(request):
    """Displays the menu with pizza options."""
    pizzas = Pizza.objects.all()
    context = {'pizzas': pizzas}
    return render(request, 'catalog/order_list.html', context=context)
