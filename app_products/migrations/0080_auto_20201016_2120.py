# Generated by Django 2.2.15 on 2020-10-16 20:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_products', '0079_auto_20201015_2230'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='purchaseorderitem',
            options={'ordering': ['product_sku']},
        ),
        migrations.RemoveField(
            model_name='purchaseorderitem',
            name='status_ordering',
        ),
    ]
