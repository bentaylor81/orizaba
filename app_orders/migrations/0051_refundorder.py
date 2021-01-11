# Generated by Django 2.2.15 on 2020-12-02 23:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_orders', '0050_orderitem_item_refunded'),
    ]

    operations = [
        migrations.CreateModel(
            name='RefundOrder',
            fields=[
                ('refundorder_id', models.IntegerField(primary_key=True, serialize=False)),
                ('refund_amount', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=7)),
                ('auth_code', models.CharField(blank=True, max_length=200)),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('order_id', models.ForeignKey(blank=True, db_column='order_id', null=True, on_delete=django.db.models.deletion.CASCADE, to='app_orders.Order')),
            ],
            options={
                'ordering': ['-date_time'],
            },
        ),
    ]