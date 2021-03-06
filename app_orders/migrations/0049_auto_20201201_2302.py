# Generated by Django 2.2.15 on 2020-12-01 23:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_orders', '0048_order_return_complete'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='inspection_passed_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='item_received_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='item_refunded_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='status_current',
            field=models.ForeignKey(blank=True, db_column='status_current', default='10', null=True, on_delete=django.db.models.deletion.CASCADE, to='app_orders.OrderStatusType'),
        ),
    ]
