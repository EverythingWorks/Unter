# Generated by Django 2.0.4 on 2018-05-28 18:03

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rides_handling', '0030_auto_20180527_1103'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Comment',
            new_name='Message',
        ),
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['date']},
        ),
    ]