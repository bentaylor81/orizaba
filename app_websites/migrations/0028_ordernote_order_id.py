# Generated by Django 3.0.6 on 2020-06-03 11:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_websites', '0027_auto_20200603_1148'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordernote',
            name='order_id',
            field=models.ForeignKey(blank=True, db_column='order_id', null=True, on_delete=django.db.models.deletion.CASCADE, to='app_websites.Order'),
        ),
    ]