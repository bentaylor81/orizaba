# Generated by Django 2.2.15 on 2020-11-28 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_orders', '0046_auto_20201128_0544'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='amount_refunded',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=7),
        ),
    ]
