# Generated by Django 2.2.15 on 2021-01-20 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_products', '0105_auto_20210120_2126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stocklocation',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]