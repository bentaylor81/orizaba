# Generated by Django 2.2.15 on 2020-11-27 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_orders', '0042_auto_20201127_2144'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='return_order',
            field=models.BooleanField(default=False),
        ),
    ]