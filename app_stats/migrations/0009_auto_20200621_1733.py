# Generated by Django 3.0.6 on 2020-06-21 16:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_stats', '0008_auto_20200621_1313'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='day',
            options={'ordering': ['day']},
        ),
        migrations.AlterModelOptions(
            name='year',
            options={'ordering': ['year']},
        ),
    ]
