# Generated by Django 3.0.6 on 2020-06-04 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_websites', '0037_auto_20200604_1304'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('brand', models.CharField(max_length=200, primary_key=True, serialize=False)),
            ],
        ),
    ]