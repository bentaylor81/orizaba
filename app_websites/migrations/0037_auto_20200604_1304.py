# Generated by Django 3.0.6 on 2020-06-04 12:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_websites', '0036_auto_20200604_1301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='supplier',
            field=models.ForeignKey(blank=True, db_column='supplier', default='Unknown', null=True, on_delete=django.db.models.deletion.CASCADE, to='app_websites.Supplier'),
        ),
    ]