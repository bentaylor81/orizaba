# Generated by Django 3.0.6 on 2020-08-01 16:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_orders', '0039_auto_20200731_2312'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orderitem',
            options={'ordering': ['item_qty']},
        ),
    ]