# Generated by Django 2.2.15 on 2020-11-05 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_orders', '0015_auto_20201105_1837'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordershipment',
            name='delivery_firstname',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='ordershipment',
            name='delivery_lastname',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]