# Generated by Django 3.0.6 on 2020-06-06 18:35

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app_websites', '0044_auto_20200606_1928'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
