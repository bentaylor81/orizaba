# Generated by Django 2.2.15 on 2020-12-04 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_orders', '0064_auto_20201204_2125'),
    ]

    operations = [
        migrations.RenameField(
            model_name='refundorder',
            old_name='refund_notes',
            new_name='refund_note',
        ),
        migrations.AlterField(
            model_name='refundorder',
            name='refund_reason',
            field=models.CharField(blank=True, choices=[('Customer Returned Order', 'Customer Returned Order'), ('Incorrect Part Sent', 'Incorrect Part Sent'), ('Faulty Part Refund', 'Faulty Part Refund'), ('Cancelled Order Refund', 'Cancelled Order Refund'), ('Duplicate Order Refund', 'Duplicate Order Refund'), ('Postage Refund Orders Combined', 'Postage Refund Orders Combined'), ('Postage Refund Other', 'Postage Refund Other'), ('Other Reason', 'Other Reason')], max_length=200),
        ),
    ]