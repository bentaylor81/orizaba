# Generated by Django 2.2.15 on 2020-10-14 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_products', '0067_product_orizaba_stock_qty'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='orizaba_init_stock_qty',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
