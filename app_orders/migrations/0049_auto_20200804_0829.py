# Generated by Django 3.0.6 on 2020-08-04 07:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_orders', '0048_auto_20200804_0817'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ordershipment',
            options={'ordering': ['-date_created']},
        ),
    ]