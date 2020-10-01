# Generated by Django 2.2.15 on 2020-09-21 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_products', '0029_auto_20200921_1641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorderitem',
            name='received_status',
            field=models.CharField(blank=True, choices=[('Pending', '1-Pending'), ('Partial', '4-Partially Received'), ('Received', '3-All Reveived')], default='Pending', max_length=200),
        ),
    ]
