# Generated by Django 2.2.15 on 2020-12-02 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_orders', '0049_auto_20201201_2302'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='item_refunded',
            field=models.BooleanField(default=False),
        ),
    ]