# Generated by Django 2.2.15 on 2020-12-15 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_orders', '0073_auto_20201214_2021'),
    ]

    operations = [
        migrations.RenameField(
            model_name='refundorderitem',
            old_name='orderitem_id',
            new_name='orderitem_id_2',
        ),
        migrations.AddField(
            model_name='refundorder',
            name='credit_note_number',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
