# Generated by Django 2.2.15 on 2021-01-24 19:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_products', '0108_auto_20210121_1242'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockSyncMagento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stock_qty', models.IntegerField(blank=True, default=0)),
                ('date_added', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_synced', models.DateTimeField(blank=True, null=True)),
                ('synced', models.BooleanField(default=True)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app_products.Product')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]