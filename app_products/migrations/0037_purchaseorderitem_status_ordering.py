# Generated by Django 2.2.15 on 2020-09-21 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_products', '0036_auto_20200921_1702'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseorderitem',
            name='status_ordering',
            field=models.IntegerField(blank=True, default=1),
        ),
    ]