# Generated by Django 2.2.15 on 2020-10-01 20:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_products', '0046_auto_20200923_2147'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='purchaseorderitem',
            options={'ordering': ['status_ordering', '-id']},
        ),
    ]
