from django.db import models
from django.contrib.auth.models import User

class Pizza(models.Model):
    pizza_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, help_text="Enter the name of the pizza")
    description = models.CharField(max_length=250, help_text="Enter the description of the pizza")
    price = models.DecimalField(max_digits=5, decimal_places=2, help_text="Enter the price of the pizza")
    image = models.ImageField(upload_to='pizza_images/', null=True, blank=True, help_text="Upload an image of the pizza")


    def __str__(self):
        return self.name

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Inherits first_name, last_name, email, password
    role = models.CharField(max_length=50, help_text="Enter the employee's role")
    phone_number = models.CharField(max_length=15, null=True, help_text="Enter the employee's phone number")

    def __str__(self):
        return self.user.username

class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Inherits first_name, last_name, email, password
    phone_number = models.CharField(max_length=15, null=True, help_text="Enter the member's phone number")
    street_address = models.CharField(max_length=50, null=True, help_text="Enter the member's street address")
    city = models.CharField(max_length=25, null=True, help_text="Enter the city")
    state = models.CharField(max_length=20, null=True, help_text="Enter the state")
    zip_code = models.CharField(max_length=10, null=True, help_text="Enter the postal code")

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Guest(models.Model):
    guest_id = models.AutoField(primary_key=True)

    def __str__(self):
        return f"Guest {self.guest_id}"

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    member = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, help_text="Member who placed the order")
    guest = models.ForeignKey(Guest, on_delete=models.SET_NULL, null=True, blank=True, help_text="Guest who placed the order")
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, help_text="Employee who placed the order")
    order_date = models.DateTimeField(auto_now_add=True, help_text="The date the order was placed")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Total amount for the order")
    order_status = models.CharField(max_length=50, help_text="Status of the order (e.g., Pending, Completed)")

    def __str__(self):
        if self.member:
            return f"Order {self.order_id} by Member: {self.member.user.username}"
        elif self.guest:
            return f"Order {self.order_id} by Guest {self.guest.guest_id}"
        elif self.employee:
            return f"Order {self.order_id} by Employee: {self.employee.user.username}"
        return f"Order {self.order_id} (No associated user)"

class OrderDetail(models.Model):
    order_detail_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, help_text="The order this detail belongs to", related_name="order_details")
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE, help_text="The pizza in this order")
    quantity = models.PositiveIntegerField(help_text="Quantity of pizzas ordered")
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, help_text="Employee who made the pizza")

    def __str__(self):
        return f"{self.quantity} x {self.pizza.name}"

class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, help_text="The order this payment is for", related_name="payments")
    card_number = models.CharField(max_length=16, help_text="Enter the card number")
    expiration_date = models.CharField(max_length=5, help_text="Enter the card's expiration date (MM/YY)")
    security_code = models.CharField(max_length=3, help_text="Enter the card's security code")
    billing_zip_code = models.CharField(max_length=10, help_text="Enter the billing zip code")

    def __str__(self):
        return f"Payment for Order {self.order.order_id}"
