# Generated by Django 3.0.6 on 2020-06-23 14:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_websites', '0039_remove_order_stats_updated'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='items_qty',
            new_name='item_qty',
        ),
    ]
