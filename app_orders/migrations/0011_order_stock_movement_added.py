# Generated by Django 2.2.15 on 2020-10-13 22:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_orders', '0010_orderdeliverymethod_service_provider_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='stock_movement_added',
            field=models.BooleanField(default=False),
        ),
    ]
