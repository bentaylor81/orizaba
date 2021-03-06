# Generated by Django 2.2.15 on 2020-11-20 04:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_utils', '0005_delete_printprocess'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrintProcess',
            fields=[
                ('process_id', models.AutoField(primary_key=True, serialize=False)),
                ('process_name', models.CharField(blank=True, max_length=200, null=True)),
                ('process_printer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app_utils.Printer')),
            ],
        ),
    ]
