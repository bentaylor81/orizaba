# Generated by Django 2.2.15 on 2021-01-12 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_utils', '0015_remove_apilog_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='apilog',
            options={'ordering': ['-id']},
        ),
        migrations.AddField(
            model_name='apilog',
            name='process',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
