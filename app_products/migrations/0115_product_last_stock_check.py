# Generated by Django 2.2.15 on 2021-01-28 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_products', '0114_auto_20210126_2140'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='last_stock_check',
            field=models.DateTimeField(null=True),
        ),
    ]