# Generated by Django 2.2.15 on 2020-11-10 04:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_orders', '0023_auto_20201110_0446'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderdeliverymethod',
            old_name='service_provider_name',
            new_name='courier',
        ),
    ]