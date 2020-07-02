# Generated by Django 3.0.6 on 2020-07-02 22:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_websites', '0058_auto_20200702_2325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='navigationsubtab',
            name='parent_tab',
            field=models.ForeignKey(blank=True, db_column='parent_tab', null=True, on_delete=django.db.models.deletion.CASCADE, to='app_websites.NavigationTab'),
        ),
    ]
