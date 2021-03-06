# Generated by Django 2.2.15 on 2020-09-21 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_products', '0035_auto_20200921_1659'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorderitem',
            name='received_status',
            field=models.CharField(blank=True, choices=[('Order Pending', 'Order Pending'), ('Partial Receipt', 'Partial Receipt'), ('Full Receipt', 'Full Receipt')], default='Order Pending', max_length=200),
        ),
    ]
