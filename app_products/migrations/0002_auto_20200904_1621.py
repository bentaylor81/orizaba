# Generated by Django 2.2.15 on 2020-09-04 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sealed_item',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='stock_qty',
            field=models.IntegerField(blank=True, choices=[(0, 'Yes')], default=0),
        ),
    ]
