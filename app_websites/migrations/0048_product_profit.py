# Generated by Django 3.0.6 on 2020-06-08 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_websites', '0047_auto_20200608_1248'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='profit',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=7),
        ),
    ]
