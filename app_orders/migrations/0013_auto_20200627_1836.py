# Generated by Django 3.0.6 on 2020-06-27 17:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_orders', '0012_remove_orderstatushistory1_billing_city'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='OrderStatusHistory1',
            new_name='OrderStatusHistory',
        ),
    ]
