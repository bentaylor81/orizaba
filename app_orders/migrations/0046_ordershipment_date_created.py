# Generated by Django 3.0.6 on 2020-08-04 06:54

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app_orders', '0045_ordershipment_tracking_ref'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordershipment',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]