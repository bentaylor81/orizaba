# Generated by Django 3.0.6 on 2020-07-02 19:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_websites', '0056_auto_20200702_1932'),
    ]

    operations = [
        migrations.RenameField(
            model_name='navigationtab',
            old_name='page_extension',
            new_name='path',
        ),
    ]