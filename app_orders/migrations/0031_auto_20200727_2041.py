# Generated by Django 3.0.6 on 2020-07-27 19:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_orders', '0030_remove_orderitem_initial_updated'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orderitem',
            options={'ordering': ['orderitem_id']},
        ),
    ]