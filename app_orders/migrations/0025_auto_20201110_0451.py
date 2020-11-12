# Generated by Django 2.2.15 on 2020-11-10 04:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_orders', '0024_auto_20201110_0447'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderdeliverymethod',
            name='courier',
            field=models.CharField(blank=True, choices=[('APC', 'APC'), ('DPD', 'DPD'), ('Royal Mail', 'Royal Mail'), ('NA', 'NA')], max_length=200),
        ),
    ]
