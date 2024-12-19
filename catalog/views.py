from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Pizza, Order, OrderDetail, Employee, Member, Guest, Payment
from django.contrib.auth.decorators import login_required

# PaymentForm Definition
class PaymentForm(forms.Form):
    card_number = forms.CharField(
        max_length=16,
        widget=forms.TextInput(attrs={'placeholder': 'Card Number'}),
        label="Card Number"
    )
    expiration_date = forms.CharField(
        max_length=5,
        widget=forms.TextInput(attrs={'placeholder': 'MM/YY'}),
        label="Expiration Date"
    )
    security_code = forms.CharField(
        max_length=3,
        widget=forms.TextInput(attrs={'placeholder': 'CVV'}),
        label="Security Code"
    )
    billing_zip_code = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={'placeholder': 'Billing ZIP Code'}),
        label="Billing ZIP Code"
    )

# Homepage
def index(request):
    context = {
        'num_pizzas': Pizza.objects.count(),
        'num_orders': Order.objects.count(),
        'num_employees': Employee.objects.count(),
        'num_members': Member.objects.count(),
    }
    return render(request, 'catalog/index.html', context=context)

# Pizza Views
class PizzaListView(generic.ListView):
    model = Pizza
    template_name = 'catalog/pizza_list.html'
    context_object_name = 'pizzas'

class PizzaDetailView(generic.DetailView):
    model = Pizza
    template_name = 'catalog/pizza_detail.html'

class PizzaCreateView(LoginRequiredMixin, CreateView):
    model = Pizza
    fields = ['name', 'description', 'price', 'image']
    template_name = 'catalog/pizza_form.html'
    success_url = reverse_lazy('pizza_list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Employee').exists():
            messages.error(request, "You do not have permission to add pizzas.")
            return redirect('pizza_list')
        return super().dispatch(request, *args, **kwargs)

class PizzaUpdateView(LoginRequiredMixin, UpdateView):
    model = Pizza
    fields = ['name', 'description', 'price', 'image']
    template_name = 'catalog/pizza_form.html'
    success_url = reverse_lazy('pizza_list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Employee').exists():
            messages.error(request, "You do not have permission to edit pizzas.")
            return redirect('pizza_list')
        return super().dispatch(request, *args, **kwargs)

class PizzaDeleteView(LoginRequiredMixin, DeleteView):
    model = Pizza
    template_name = 'catalog/pizza_confirm_delete.html'
    success_url = reverse_lazy('pizza_list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Employee').exists():
            messages.error(request, "You do not have permission to delete pizzas.")
            return redirect('pizza_list')
        return super().dispatch(request, *args, **kwargs)

# Cart Views
@login_required
def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for pizza_id, quantity in cart.items():
        try:
            pizza = Pizza.objects.get(pizza_id=pizza_id)
            cart_items.append({
                'pizza': pizza,
                'quantity': quantity,
                'subtotal': pizza.price * quantity
            })
            total += pizza.price * quantity
        except Pizza.DoesNotExist:
            continue

    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'catalog/cart.html', context)

@login_required
def add_to_cart(request, pizza_id):
    try:
        pizza = Pizza.objects.get(pizza_id=pizza_id)
        cart = request.session.get('cart', {})
        cart[str(pizza_id)] = cart.get(str(pizza_id), 0) + 1
        request.session['cart'] = cart
        messages.success(request, f"{pizza.name} added to cart!")
    except Pizza.DoesNotExist:
        messages.error(request, "Invalid pizza ID.")
    return redirect('cart')

@login_required
def remove_from_cart(request, pizza_id):
    try:
        pizza = Pizza.objects.get(pizza_id=pizza_id)
        cart = request.session.get('cart', {})

        if str(pizza_id) in cart:
            if cart[str(pizza_id)] > 1:
                cart[str(pizza_id)] -= 1
                messages.success(request, f"One {pizza.name} removed from cart.")
            else:
                del cart[str(pizza_id)]
                messages.success(request, f"{pizza.name} removed from cart.")
            request.session['cart'] = cart
        else:
            messages.error(request, f"{pizza.name} is not in the cart.")
    except Pizza.DoesNotExist:
        messages.error(request, "Invalid pizza ID.")

    return redirect('cart')

# Payment Views
@login_required
def payment_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for pizza_id, quantity in cart.items():
        try:
            pizza = Pizza.objects.get(pizza_id=pizza_id)
            cart_items.append({
                'pizza': pizza,
                'quantity': quantity,
                'subtotal': pizza.price * quantity
            })
            total += pizza.price * quantity
        except Pizza.DoesNotExist:
            continue

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                member=Member.objects.filter(user=request.user).first(),
                total_amount=total,
                order_status="Completed"
            )

            for item in cart_items:
                OrderDetail.objects.create(
                    order=order,
                    pizza=item['pizza'],
                    quantity=item['quantity']
                )

            Payment.objects.create(
                order=order,
                card_number=form.cleaned_data['card_number'],
                expiration_date=form.cleaned_data['expiration_date'],
                security_code=form.cleaned_data['security_code'],
                billing_zip_code=form.cleaned_data['billing_zip_code']
            )

            messages.success(request, "Payment successful! Order has been created.")
            request.session['cart'] = {}
            return redirect('index')
    else:
        form = PaymentForm()

    context = {
        'cart_items': cart_items,
        'total': total,
        'form': form,
    }
    return render(request, 'catalog/payment.html', context)


@login_required
def process_payment(request):
    """Handles payment submission."""
    if request.method == 'POST':
        messages.success(request, "Payment processed successfully!")
        request.session['cart'] = {}
        return redirect('index')
    else:
        messages.error(request, "Invalid request method for payment.")
        return redirect('payment')



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
    fields = ['member', 'guest', 'total_amount', 'order_status']  # Fields for creating an order
    template_name = 'catalog/order_form.html'  # Ensure this template exists
    success_url = reverse_lazy('order_list')  # Redirect to the order list after successful creation

    def form_valid(self, form):
        """Set the employee as the logged-in user."""
        # Automatically associate the logged-in employee with the order
        if hasattr(self.request.user, 'employee'):
            form.instance.employee = self.request.user.employee
        messages.success(self.request, "Order created successfully!")
        return super().form_valid(form)

class OrderUpdateView(LoginRequiredMixin, UpdateView):
    """Allows updating an existing order."""
    model = Order
    fields = ['member', 'guest', 'total_amount', 'order_status']  # Fields that can be updated
    template_name = 'catalog/order_form.html'  # Reuse the form template for order creation and updates
    success_url = reverse_lazy('order_list')  # Redirect to the order list after successful update

    def form_valid(self, form):
        """Set the employee as the logged-in user when updating."""
        if hasattr(self.request.user, 'employee'):
            form.instance.employee = self.request.user.employee
        messages.success(self.request, "Order updated successfully!")
        return super().form_valid(form)

class OrderDeleteView(LoginRequiredMixin, DeleteView):
    """Allows deletion of an order."""
    model = Order
    template_name = 'catalog/order_confirm_delete.html'  # Template for confirmation
    success_url = reverse_lazy('order_list')  # Redirect to the order list after deletion

    def delete(self, request, *args, **kwargs):
        """Override delete to add custom messages."""
        messages.success(self.request, "Order deleted successfully!")
        return super().delete(request, *args, **kwargs)

class MemberListView(LoginRequiredMixin, generic.ListView):
    """Displays a list of all members."""
    model = Member
    template_name = 'catalog/member_list.html'  # Path to the template for listing members
    context_object_name = 'members'  # Name of the context variable in the template

class MemberDetailView(LoginRequiredMixin, generic.DetailView):
    """Displays detailed information about a specific member."""
    model = Member
    template_name = 'catalog/member_detail.html'  # Path to the template for member details
    context_object_name = 'member'  # Name of the context variable in the template


class MemberCreateView(LoginRequiredMixin, CreateView):
    """Allows creation of a new member."""
    model = Member
    fields = ['phone_number', 'street_address', 'city', 'state', 'zip_code']  # Fields for creating a member
    template_name = 'catalog/member_form.html'  # Template for member creation form
    success_url = reverse_lazy('member_list')  # Redirect to the member list after successful creation

    def form_valid(self, form):
        """Link the newly created member to the logged-in user."""
        form.instance.user = self.request.user
        messages.success(self.request, "Member created successfully!")
        return super().form_valid(form)


class MemberUpdateView(LoginRequiredMixin, UpdateView):
    """Allows updating an existing member."""
    model = Member
    fields = ['phone_number', 'street_address', 'city', 'state', 'zip_code']  # Fields that can be updated
    template_name = 'catalog/member_form.html'  # Reuse the member creation template
    success_url = reverse_lazy('member_list')  # Redirect to the member list after successful update

    def form_valid(self, form):
        """Ensure that the logged-in user can only update their own member profile."""
        if form.instance.user != self.request.user:
            messages.error(self.request, "You can only update your own profile.")
            return redirect('member_list')
        messages.success(self.request, "Member updated successfully!")
        return super().form_valid(form)

class MemberDeleteView(LoginRequiredMixin, DeleteView):
    """Allows deletion of a member."""
    model = Member
    template_name = 'catalog/member_confirm_delete.html'  # Template for delete confirmation
    success_url = reverse_lazy('member_list')  # Redirect to member list after deletion

    def delete(self, request, *args, **kwargs):
        """Ensure the logged-in user can only delete their own member profile."""
        member = self.get_object()
        if member.user != self.request.user:
            messages.error(self.request, "You can only delete your own profile.")
            return redirect('member_list')
        messages.success(self.request, "Member deleted successfully!")
        return super().delete(request, *args, **kwargs)
