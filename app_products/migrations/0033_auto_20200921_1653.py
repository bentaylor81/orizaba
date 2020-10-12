# Generated by Django 2.2.15 on 2020-09-21 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_products', '0032_auto_20200921_1651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorderitem',
            name='received_status',
            field=models.CharField(blank=True, choices=[('Order Pending', 'Received All Items'), ('Partially Received', 'Partially Items'), ('Received All Items', 'Received All Items')], default='Order Pending', max_length=200),
        ),
    ]