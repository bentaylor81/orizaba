# Generated by Django 2.2.15 on 2020-12-14 20:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_orders', '0072_auto_20201210_1937'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='refundorderitem',
            options={'ordering': ['xero_line_item']},
        ),
    ]