# Generated by Django 2.2.15 on 2020-11-06 18:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_orders', '0018_ordershipment_shipment_no'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ordershipment',
            old_name='shipment_no',
            new_name='shipping_ref',
        ),
    ]