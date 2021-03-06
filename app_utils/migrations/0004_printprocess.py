# Generated by Django 2.2.15 on 2020-11-20 04:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_utils', '0003_auto_20201120_0431'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrintProcess',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('process_name', models.CharField(blank=True, max_length=200, null=True)),
                ('process_printer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app_utils.Printer')),
            ],
        ),
    ]
