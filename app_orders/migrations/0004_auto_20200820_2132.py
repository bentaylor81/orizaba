# Generated by Django 3.0.6 on 2020-08-20 20:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_orders', '0003_order_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['date']},
        ),
    ]