# Generated by Django 2.2.15 on 2020-09-04 15:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_orders', '0006_remove_order_ip_address'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-date']},
        ),
    ]
