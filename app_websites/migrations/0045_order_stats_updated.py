# Generated by Django 3.0.6 on 2020-06-23 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_websites', '0044_auto_20200623_1524'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='stats_updated',
            field=models.BooleanField(default=True),
        ),
    ]
