# Generated by Django 2.2.15 on 2020-10-13 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_orders', '0012_remove_order_stock_movement_added'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='stock_movement_added',
            field=models.BooleanField(default=False),
        ),
    ]
