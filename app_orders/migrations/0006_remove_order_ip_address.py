# Generated by Django 3.0.6 on 2020-08-21 07:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_orders', '0005_remove_order_stats_updated'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='ip_address',
        ),
    ]
