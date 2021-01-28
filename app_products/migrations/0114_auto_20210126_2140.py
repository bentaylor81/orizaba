# Generated by Django 2.2.15 on 2021-01-26 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_products', '0113_auto_20210126_2130'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stockcheck',
            old_name='current_stock_qty',
            new_name='actual_qty',
        ),
        migrations.RenameField(
            model_name='stockcheck',
            old_name='new_stock_qty',
            new_name='expected_qty',
        ),
        migrations.AddField(
            model_name='stockcheck',
            name='difference_qty',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
