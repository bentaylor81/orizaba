# Generated by Django 2.2.15 on 2021-01-13 14:46

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app_products', '0088_auto_20210113_1439'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseorderitem',
            name='date_updated_2',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
