# Generated by Django 3.0.6 on 2020-06-23 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_stats', '0010_remove_month_month'),
    ]

    operations = [
        migrations.AddField(
            model_name='month',
            name='month',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]