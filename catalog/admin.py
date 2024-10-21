from django.contrib import admin
from .models import Pizza, Employee, Member, Guest, Order, OrderDetail, Payment

# Register your models here.
admin.site.register(Pizza)
admin.site.register(Employee)
admin.site.register(Member)
admin.site.register(Guest)
admin.site.register(Order)
admin.site.register(OrderDetail)
admin.site.register(Payment)
