# Generated by Django 2.2.15 on 2020-09-05 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_orders', '0007_auto_20200904_1621'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='invoice_created',
            field=models.BooleanField(default=True),
        ),
    ]
