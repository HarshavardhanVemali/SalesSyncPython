# Generated by Django 5.1.3 on 2024-12-03 17:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BillSequence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('area', models.CharField(max_length=255)),
                ('phone', models.CharField(blank=True, max_length=15, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='FailedLoginAttempts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_id', models.CharField(max_length=255, unique=True)),
                ('attempts', models.PositiveBigIntegerField(default=0)),
                ('is_active', models.BooleanField(default=False)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bill_no', models.CharField(editable=False, max_length=50, unique=True)),
                ('product', models.CharField(max_length=255)),
                ('billing_date', models.DateField()),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_paid', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('balance', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(choices=[('paid', 'Paid'), ('partially_paid', 'Partially Paid'), ('unpaid', 'Unpaid')], default='unpaid', max_length=20)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_date', models.DateField()),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('paid_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_method', models.CharField(choices=[('cash', 'Cash'), ('card', 'Card'), ('cheque', 'Cheque'), ('upi', 'UPI'), ('bank_transfer', 'Bank Transfer')], max_length=50)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.order')),
            ],
        ),
    ]
