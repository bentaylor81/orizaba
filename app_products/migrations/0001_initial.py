# Generated by Django 3.0.6 on 2020-08-20 14:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('brand', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('path', models.CharField(blank=True, max_length=200)),
            ],
            options={
                'ordering': ['brand'],
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('customer_id', models.AutoField(primary_key=True, serialize=False)),
                ('billing_email', models.CharField(blank=True, max_length=200, unique=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('supplier', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('path', models.CharField(blank=True, max_length=200)),
                ('sort_order', models.IntegerField(default=100)),
            ],
            options={
                'ordering': ['sort_order'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('product_id', models.IntegerField(primary_key=True, serialize=False)),
                ('product_name', models.CharField(blank=True, max_length=200)),
                ('sku', models.CharField(blank=True, max_length=200)),
                ('buy_price', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=7)),
                ('sell_price', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=7)),
                ('stock_qty', models.IntegerField(blank=True, default=0)),
                ('item_profit', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=7)),
                ('stock_profit', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=7)),
                ('buy_value', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=7)),
                ('sell_value', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=7)),
                ('profit_margin', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=7)),
                ('weight', models.DecimalField(blank=True, decimal_places=4, default=0, max_digits=7)),
                ('location', models.CharField(blank=True, default='null', max_length=200)),
                ('part_type', models.CharField(blank=True, default='null', max_length=200)),
                ('url', models.CharField(blank=True, default='null', max_length=200)),
                ('image', models.CharField(blank=True, default='null', max_length=200)),
                ('condition', models.CharField(blank=True, default='new', max_length=200)),
                ('special_order', models.CharField(blank=True, default='no', max_length=200)),
                ('brand', models.ForeignKey(blank=True, db_column='brand', default='Other', null=True, on_delete=django.db.models.deletion.CASCADE, to='app_products.Brand')),
                ('supplier', models.ForeignKey(blank=True, db_column='supplier', default='Unknown', null=True, on_delete=django.db.models.deletion.CASCADE, to='app_products.Supplier')),
            ],
            options={
                'ordering': ['product_id', 'location'],
            },
        ),
    ]
