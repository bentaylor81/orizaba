# Generated by Django 3.0.6 on 2020-06-27 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_orders', '0014_auto_20200627_1841'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderstatustype',
            name='icon',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]