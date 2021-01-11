# Generated by Django 2.2.15 on 2020-12-04 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_orders', '0063_auto_20201204_1828'),
    ]

    operations = [
        migrations.AlterField(
            model_name='refundorder',
            name='refund_reason',
            field=models.CharField(blank=True, choices=[('01', 'Customer Returned Order'), ('02', 'Incorrect Part Sent'), ('03', 'Faulty Part Refund'), ('04', 'Cancelled Order Refund'), ('05', 'Duplicate Order Refund'), ('06', 'Postage Refund Orders Combined'), ('07', 'Postage Refund Other'), ('08', 'Other Reason')], max_length=200),
        ),
    ]