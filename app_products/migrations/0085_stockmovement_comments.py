# Generated by Django 2.2.15 on 2020-10-21 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_products', '0084_auto_20201020_1844'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockmovement',
            name='comments',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
