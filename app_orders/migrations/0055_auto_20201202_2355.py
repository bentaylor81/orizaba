# Generated by Django 2.2.15 on 2020-12-02 23:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_orders', '0054_refundorder'),
    ]

    operations = [
        migrations.AddField(
            model_name='refundorder',
            name='email_customer',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='refundorder',
            name='sagepay_refund',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='refundorder',
            name='xero_credit_note',
            field=models.BooleanField(default=True),
        ),
    ]