# Generated by Django 3.0.6 on 2020-07-05 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_orders', '0026_orderitem_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='send_qty',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='updated',
            field=models.BooleanField(default=False),
        ),
    ]
