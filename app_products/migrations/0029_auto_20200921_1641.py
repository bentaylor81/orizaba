# Generated by Django 2.2.15 on 2020-09-21 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_products', '0028_auto_20200921_1639'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorderitem',
            name='received_status',
            field=models.CharField(blank=True, choices=[('1-Pending', 'Pending'), ('4-Partially Received', 'Partial'), ('3-All Reveived', 'Received')], default='Pending', max_length=200),
        ),
    ]
