# Generated by Django 2.2.15 on 2021-02-02 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_products', '0123_productlabel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productlabel',
            name='qty',
            field=models.PositiveIntegerField(blank=True),
        ),
    ]
