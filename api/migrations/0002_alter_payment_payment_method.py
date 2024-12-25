# Generated by Django 5.1.3 on 2024-12-24 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_method',
            field=models.CharField(choices=[('cash', 'Cash'), ('card', 'Card'), ('cheque', 'Cheque'), ('upi', 'UPI'), ('bank_transfer', 'Bank Transfer'), ('deafult', 'Default')], max_length=50),
        ),
    ]