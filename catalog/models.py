from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import uuid

class Pizza(models.Model):
    pizza_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, help_text="Enter the name of the pizza")
    description = models.CharField(max_length=250, help_text="Enter the description of the pizza")
    price = models.DecimalField(max_digits=5, decimal_places=2, help_text="Enter the price of the pizza")
    size = models.CharField(max_length=50, help_text="Enter the size of the pizza (e.g., Small, Medium, Large)")

    def __str__(self):
        return self.name

class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, help_text="Link to the Django User table")
    role = models.CharField(max_length=50, help_text="Enter the employee's role (e.g., Manager, Cashier)")

    def __str__(self):
        return self.user.username

class Member(models.Model):
    member_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, help_text="Link to the Django User table")
    address = models.CharField(max_length=250, help_text="Enter the member's address")

    def __str__(self):
        return self.user.username

class Guest(models.Model):
    guest_id = models.AutoField(primary_key=True)
    session_id = models.CharField(max_length=100, help_text="Enter the session ID for the guest")

    def __str__(self):
        return self.session_id

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    member = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, help_text="The member who placed the order")
    order_date = models.DateTimeField(auto_now_add=True, help_text="The date the order was placed")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Total amount for the order")
    order_status = models.CharField(max_length=50, help_text="Status of the order (e.g., Pending, Completed)")

    def __str__(self):
        return f"Order {self.id} by {self.member.username}"

class OrderDetail(models.Model):
    order_detail_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, help_text="The order this detail belongs to")
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE, help_text="The pizza in this order")
    quantity = models.PositiveIntegerField(help_text="Quantity of pizzas ordered")
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, help_text="Employee who made the pizza")

    def __str__(self):
        return f"{self.quantity} x {self.pizza.name}"

class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, help_text="The order this payment is for")
    card_number = models.CharField(max_length=16, help_text="Enter the card number")
    expiration_date = models.CharField(max_length=5, help_text="Enter the card's expiration date (MM/YY)")
    security_code = models.CharField(max_length=3, help_text="Enter the card's security code")
    billing_zip_code = models.CharField(max_length=10, help_text="Enter the billing zip code")

    def __str__(self):
        return f"Payment for Order {self.order.id}"
