# Generated by Django 3.0.6 on 2020-06-27 17:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_orders', '0008_orderstatushistory1_status_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderstatushistory1',
            name='status_type',
        ),
    ]