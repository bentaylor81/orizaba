# Generated by Django 3.0.6 on 2020-06-28 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_orders', '0019_auto_20200628_1910'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderstatushistory',
            name='test_test',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
