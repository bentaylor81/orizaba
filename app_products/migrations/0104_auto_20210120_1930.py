# Generated by Django 2.2.15 on 2021-01-20 19:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_products', '0103_product_location_v2'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stocklocation',
            old_name='product_id',
            new_name='product',
        ),
    ]
