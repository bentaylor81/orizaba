# Generated by Django 3.0.6 on 2020-06-02 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_websites', '0022_auto_20200524_2118'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderNote',
            fields=[
                ('ordernote_id', models.IntegerField(primary_key=True, serialize=False)),
                ('note', models.TextField(blank=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['date'],
            },
        ),
    ]
