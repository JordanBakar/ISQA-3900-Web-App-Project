from django.contrib import admin
from .models import Pizza, Employee, Member, Guest, Order, OrderDetail, Payment

# Custom Admin for Pizza
@admin.register(Pizza)
class PizzaAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description')  # Fields to display in list view
    search_fields = ('name', 'description')  # Enable search by name and description
    list_filter = ('price',)  # Filter by price


# Custom Admin for Employee
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'phone_number')  # Display these fields in list view
    search_fields = ('user__username', 'role')  # Enable search by username and role
    list_filter = ('role',)  # Filter by role


# Custom Admin for Member
@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'city', 'state', 'zip_code')  # Display these fields in list view
    search_fields = ('user__username', 'phone_number', 'city')  # Enable search
    list_filter = ('state',)  # Filter by state


# Custom Admin for Guest
@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ('guest_id',)  # Display guest_id


# Custom Admin for Order
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'member', 'guest', 'total_amount', 'order_status', 'order_date')  # List view fields
    search_fields = ('order_id', 'member__user__username', 'guest__guest_id')  # Enable search
    list_filter = ('order_status', 'order_date')  # Filter by status and date


# Custom Admin for OrderDetail
@admin.register(OrderDetail)
class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ('order', 'pizza', 'quantity', 'employee')  # Display these fields in list view
    search_fields = ('order__order_id', 'pizza__name', 'employee__user__username')  # Enable search


# Custom Admin for Payment
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'order', 'card_number', 'expiration_date', 'billing_zip_code')  # Display fields
    search_fields = ('order__order_id', 'card_number')  # Enable search
