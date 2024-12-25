# models.py

from django.db import models
from django.core.exceptions import ValidationError
import uuid
from decimal import Decimal
from django.utils import timezone
from datetime import datetime
class FailedLoginAttempts(models.Model):
    device_id = models.CharField(max_length=255, unique=True)
    attempts = models.PositiveBigIntegerField(default=0)
    is_active = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.device_id} - Attempts: {self.attempts}'
    
class BillSequence(models.Model):
    current = models.IntegerField(default=1)

    @classmethod
    def get_next(cls):
        sequence, _ = cls.objects.get_or_create(id=1)
        next_number = sequence.current
        sequence.current += 1
        sequence.save()
        return next_number

class Customer(models.Model):
    name = models.CharField(max_length=255)
    area = models.CharField(max_length=255)
    phone = models.CharField(max_length=15, blank=True, null=True,unique=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    bill_no = models.CharField(max_length=50,editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.CharField(max_length=255)
    billing_date = models.DateField()
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[
        ('paid', 'Paid'),
        ('partially_paid', 'Partially Paid'),
        ('unpaid', 'Unpaid'),
    ], default='unpaid')
    class Meta:
        unique_together = ('bill_no','id')
    def save(self, *args, **kwargs):
        if not self.bill_no:
            next_sequence = BillSequence.get_next()
            self.bill_no = f"ORD{str(next_sequence).zfill(5)}"
        self.balance = self.amount - self.total_paid
        self.status = (
            'paid' if self.balance <= 0 else
            'partially_paid' if self.total_paid > 0 else
            'unpaid'
        )
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Order {self.bill_no} for {self.customer.name}"

class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_date = models.DateField()
    created_time = models.DateTimeField(auto_now_add=True)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=[
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('cheque','Cheque'),
        ('upi','UPI'),
        ('bank_transfer', 'Bank Transfer'),
        ('default','Default')
    ])
    remarks = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        order = self.order
        order.total_paid += self.paid_amount
        order.save()

    def __str__(self):
        return f"Payment of {self.paid_amount} for Order {self.order.bill_no}"

class Supplier(models.Model):
    name = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255, blank=True, null=True)  # Optional company name
    address = models.TextField(blank=True, null=True)  # Address for the supplier
    phone = models.CharField(max_length=15, blank=True, null=True, unique=True)
    email = models.EmailField(blank=True, null=True, unique=True)  # Optional unique email for contact
    gst_number = models.CharField(max_length=20, blank=True, null=True, unique=True)  # GST or tax ID

    def __str__(self):
        return self.name


class Acquisition(models.Model):
    invoice_no = models.CharField(max_length=50, editable=False)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE) 
    product = models.CharField(max_length=255)
    purchase_date = models.DateField()
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[
        ('paid', 'Paid'),
        ('partially_paid', 'Partially Paid'),
        ('unpaid', 'Unpaid'),
    ], default='unpaid')

    class Meta:
        unique_together = ('invoice_no', 'id')

    def __str__(self):
        return f"Acquisition {self.invoice_no} from {self.supplier.name}"

class AcquisitionPayment(models.Model):
    acquisition = models.ForeignKey(Acquisition, on_delete=models.CASCADE)
    payment_date = models.DateField()
    created_time = models.DateTimeField(auto_now_add=True)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=[
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('cheque', 'Cheque'),
        ('upi', 'UPI'),
        ('bank_transfer', 'Bank Transfer'),
        ('default', 'Default')
    ])
    remarks = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        acquisition = self.acquisition
        acquisition.total_paid += self.paid_amount
        acquisition.save()

    def __str__(self):
        return f"Payment of {self.paid_amount} for Acquisition {self.acquisition.invoice_no}"