# Generated by Django 3.0.6 on 2020-08-19 20:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_orders', '0053_auto_20200806_2240'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='send_qty_init_updated',
        ),
    ]