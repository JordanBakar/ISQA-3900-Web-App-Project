# Generated by Django 5.1.2 on 2024-10-21 20:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Guest',
            fields=[
                ('guest_id', models.AutoField(primary_key=True, serialize=False)),
                ('session_id', models.CharField(help_text='Enter the session ID for the guest', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Pizza',
            fields=[
                ('pizza_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='Enter the name of the pizza', max_length=100)),
                ('description', models.CharField(help_text='Enter the description of the pizza', max_length=250)),
                ('price', models.DecimalField(decimal_places=2, help_text='Enter the price of the pizza', max_digits=5)),
                ('size', models.CharField(help_text='Enter the size of the pizza (e.g., Small, Medium, Large)', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('employee_id', models.AutoField(primary_key=True, serialize=False)),
                ('role', models.CharField(help_text="Enter the employee's role (e.g., Manager, Cashier)", max_length=50)),
                ('user', models.OneToOneField(help_text='Link to the Django User table', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('member_id', models.AutoField(primary_key=True, serialize=False)),
                ('address', models.CharField(help_text="Enter the member's address", max_length=250)),
                ('user', models.OneToOneField(help_text='Link to the Django User table', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.AutoField(primary_key=True, serialize=False)),
                ('order_date', models.DateTimeField(auto_now_add=True, help_text='The date the order was placed')),
                ('total_amount', models.DecimalField(decimal_places=2, help_text='Total amount for the order', max_digits=10)),
                ('order_status', models.CharField(help_text='Status of the order (e.g., Pending, Completed)', max_length=50)),
                ('member', models.ForeignKey(help_text='The member who placed the order', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('payment_id', models.AutoField(primary_key=True, serialize=False)),
                ('card_number', models.CharField(help_text='Enter the card number', max_length=16)),
                ('expiration_date', models.CharField(help_text="Enter the card's expiration date (MM/YY)", max_length=5)),
                ('security_code', models.CharField(help_text="Enter the card's security code", max_length=3)),
                ('billing_zip_code', models.CharField(help_text='Enter the billing zip code', max_length=10)),
                ('order', models.ForeignKey(help_text='The order this payment is for', on_delete=django.db.models.deletion.CASCADE, to='catalog.order')),
            ],
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('order_detail_id', models.AutoField(primary_key=True, serialize=False)),
                ('quantity', models.PositiveIntegerField(help_text='Quantity of pizzas ordered')),
                ('employee', models.ForeignKey(help_text='Employee who made the pizza', null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.employee')),
                ('order', models.ForeignKey(help_text='The order this detail belongs to', on_delete=django.db.models.deletion.CASCADE, to='catalog.order')),
                ('pizza', models.ForeignKey(help_text='The pizza in this order', on_delete=django.db.models.deletion.CASCADE, to='catalog.pizza')),
            ],
        ),
    ]