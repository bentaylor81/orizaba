# Generated by Django 2.2.15 on 2020-10-12 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_products', '0053_auto_20201012_2128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_image',
            field=models.ImageField(blank=True, default='img/no-image.png', null=True, upload_to='media/images/products'),
        ),
    ]
