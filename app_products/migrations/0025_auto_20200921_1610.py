# Generated by Django 2.2.15 on 2020-09-21 15:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_products', '0024_auto_20200919_1034'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='purchaseorderitem',
            options={'ordering': ['items_received', 'product__sku']},
        ),
    ]
