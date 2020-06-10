# Generated by Django 3.0.6 on 2020-06-10 23:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_websites', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='customer_id',
            field=models.IntegerField(blank=True, default=1, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customer',
            name='billing_email',
            field=models.CharField(blank=True, max_length=200, primary_key=True, serialize=False),
        ),
    ]
