# Generated by Django 2.2.15 on 2020-10-03 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_products', '0049_auto_20201003_1623'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseorderitem',
            name='product_sku',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]