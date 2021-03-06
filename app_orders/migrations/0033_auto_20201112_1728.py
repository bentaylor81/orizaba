# Generated by Django 2.2.15 on 2020-11-12 17:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_orders', '0032_remove_ordershipment_delivery_method'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orderitem',
            options={'ordering': ['-order_id__date', 'orderitem_id', '-send_qty']},
        ),
        migrations.RemoveField(
            model_name='order',
            name='date_sent',
        ),
        migrations.RemoveField(
            model_name='order',
            name='delivery_method',
        ),
    ]
