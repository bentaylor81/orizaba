# Generated by Django 2.2.15 on 2020-09-23 14:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_products', '0043_auto_20200921_1946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='status',
            field=models.CharField(blank=True, choices=[('Pending', 'Pending'), ('Part Receipt', 'Part Receipt'), ('Unleashed', 'Unleashed'), ('Complete', 'Complete')], max_length=200),
        ),
        migrations.AlterField(
            model_name='purchaseorderitem',
            name='product',
            field=models.ForeignKey(default=3424, on_delete=django.db.models.deletion.CASCADE, to='app_products.Product'),
            preserve_default=False,
        ),
    ]
