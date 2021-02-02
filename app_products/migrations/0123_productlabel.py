# Generated by Django 2.2.15 on 2021-02-02 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_products', '0122_auto_20210202_1438'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductLabel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sku', models.CharField(blank=True, max_length=200)),
                ('part_type', models.CharField(blank=True, default='null', max_length=200)),
                ('qty', models.PositiveIntegerField(blank=True, max_length=200)),
                ('location', models.CharField(blank=True, max_length=200, null=True)),
                ('is_printed', models.BooleanField(default=False)),
                ('date_printed', models.DateField(auto_now_add=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]