# Generated by Django 3.0.6 on 2020-06-05 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_websites', '0041_auto_20200604_2046'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplier',
            name='sort_order',
            field=models.IntegerField(default=0),
        ),
    ]