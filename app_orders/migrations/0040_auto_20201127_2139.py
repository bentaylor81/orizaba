# Generated by Django 2.2.15 on 2020-11-27 21:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_orders', '0039_auto_20201127_2114'),
    ]

    operations = [
        migrations.DeleteModel(
            name='OrderFlag',
        ),
        migrations.RemoveField(
            model_name='order',
            name='order_status',
        ),
    ]
