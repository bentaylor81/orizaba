# Generated by Django 2.2.15 on 2020-09-21 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_products', '0038_auto_20200921_1711'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseorder',
            name='date_ordered',
            field=models.DateField(blank=True, null=True),
        ),
    ]
