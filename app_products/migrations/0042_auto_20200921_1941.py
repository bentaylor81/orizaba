# Generated by Django 2.2.15 on 2020-09-21 18:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_products', '0041_remove_purchaseorder_date_added'),
    ]

    operations = [
        migrations.RenameField(
            model_name='purchaseorder',
            old_name='date_added2',
            new_name='date_added',
        ),
    ]
