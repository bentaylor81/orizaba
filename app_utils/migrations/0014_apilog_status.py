# Generated by Django 2.2.15 on 2021-01-12 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_utils', '0013_apilog'),
    ]

    operations = [
        migrations.AddField(
            model_name='apilog',
            name='status',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]