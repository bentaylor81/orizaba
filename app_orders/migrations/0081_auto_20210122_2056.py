# Generated by Django 2.2.15 on 2021-01-22 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_orders', '0080_auto_20210121_1247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderstatushistory',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
