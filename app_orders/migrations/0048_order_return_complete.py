# Generated by Django 2.2.15 on 2020-11-28 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_orders', '0047_order_amount_refunded'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='return_complete',
            field=models.BooleanField(default=False),
        ),
    ]