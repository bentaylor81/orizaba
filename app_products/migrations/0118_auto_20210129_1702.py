# Generated by Django 2.2.15 on 2021-01-29 17:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_products', '0117_auto_20210129_1545'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='magentoproductsync',
            options={'ordering': ['-has_synced', '-id']},
        ),
    ]