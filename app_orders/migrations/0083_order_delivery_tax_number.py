# Generated by Django 2.2.15 on 2021-01-26 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_orders', '0082_auto_20210122_2057'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_tax_number',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
    ]
