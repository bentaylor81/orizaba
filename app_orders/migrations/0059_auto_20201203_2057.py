# Generated by Django 2.2.15 on 2020-12-03 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_orders', '0058_refundorderitem_refund_note'),
    ]

    operations = [
        migrations.AlterField(
            model_name='refundorderitem',
            name='orderitem_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
