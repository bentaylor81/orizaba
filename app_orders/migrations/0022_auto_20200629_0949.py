# Generated by Django 3.0.6 on 2020-06-29 08:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_orders', '0021_auto_20200629_0949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderstatushistory',
            name='order_id',
            field=models.ForeignKey(blank=True, db_column='order_id', null=True, on_delete=django.db.models.deletion.CASCADE, to='app_orders.Order'),
        ),
        migrations.AlterField(
            model_name='orderstatushistory',
            name='status_type',
            field=models.ForeignKey(blank=True, db_column='status_type', null=True, on_delete=django.db.models.deletion.CASCADE, to='app_orders.OrderStatusType'),
        ),
    ]
