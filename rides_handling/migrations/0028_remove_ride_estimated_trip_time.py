# Generated by Django 2.0.4 on 2018-05-26 23:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rides_handling', '0027_merge_20180524_1952'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ride',
            name='estimated_trip_time',
        ),
    ]
