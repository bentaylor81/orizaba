# Generated by Django 2.2.15 on 2020-09-18 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_products', '0017_auto_20200918_2016'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseorderitem',
            name='date_updated',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]