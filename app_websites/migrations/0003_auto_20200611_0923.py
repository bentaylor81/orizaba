# Generated by Django 3.0.6 on 2020-06-11 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_websites', '0002_customer2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer2',
            name='billing_email',
            field=models.CharField(blank=True, max_length=200, unique=True),
        ),
    ]