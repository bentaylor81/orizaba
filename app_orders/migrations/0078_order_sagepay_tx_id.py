# Generated by Django 2.2.15 on 2020-12-24 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_orders', '0077_auto_20201215_2133'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='sagepay_tx_id',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
