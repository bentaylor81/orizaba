# Generated by Django 3.0.6 on 2020-06-28 17:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_orders', '0016_orderstatustype_icon_color'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['date', 'time']},
        ),
        migrations.AlterModelOptions(
            name='orderstatushistory',
            options={'ordering': ['-date']},
        ),
    ]
