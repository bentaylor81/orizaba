# Generated by Django 3.0.6 on 2020-06-27 17:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_orders', '0004_orderstatushistory1'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderstatushistory1',
            name='date',
        ),
    ]