# Generated by Django 2.2.15 on 2021-01-22 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_orders', '0081_auto_20210122_2056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderstatushistory',
            name='date',
            field=models.DateTimeField(null=True),
        ),
    ]