# Generated by Django 2.2.15 on 2020-11-10 05:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_orders', '0026_ordershipment_service_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordershipment',
            name='service_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app_orders.OrderDeliveryMethod'),
        ),
    ]
