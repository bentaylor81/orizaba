# Generated by Django 2.2.15 on 2020-10-03 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_products', '0048_purchaseorder_label'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchaseorder',
            name='label',
        ),
        migrations.AddField(
            model_name='purchaseorderitem',
            name='label',
            field=models.BooleanField(default=False),
        ),
    ]