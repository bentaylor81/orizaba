# Generated by Django 2.2.15 on 2020-10-15 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_products', '0070_remove_product_orizaba_initial_stock_qty'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockmovement',
            name='current_stock_qty',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
