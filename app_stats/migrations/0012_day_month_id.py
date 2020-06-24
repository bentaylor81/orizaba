# Generated by Django 3.0.6 on 2020-06-23 18:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_stats', '0011_month_month'),
    ]

    operations = [
        migrations.AddField(
            model_name='day',
            name='month_id',
            field=models.ForeignKey(blank=True, db_column='month_id', default=201612, null=True, on_delete=django.db.models.deletion.CASCADE, to='app_stats.Month'),
        ),
    ]