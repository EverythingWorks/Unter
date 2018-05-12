# Generated by Django 2.0.4 on 2018-05-12 09:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rides_handling', '0021_ride_driver'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ride',
            name='driver',
            field=models.ForeignKey(blank=True, default=0, on_delete=django.db.models.deletion.CASCADE, related_name='driver', to='rides_handling.Profile'),
        ),
    ]
