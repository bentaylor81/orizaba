# Generated by Django 3.0.6 on 2020-06-03 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_websites', '0025_auto_20200603_1133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordernote',
            name='added_by',
            field=models.CharField(max_length=10),
        ),
    ]