# Generated by Django 2.2.15 on 2020-10-15 20:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_orders', '0013_orderitem_stock_movement_added'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orderitem',
            options={'ordering': ['-order_id__date', '-send_qty']},
        ),
    ]
