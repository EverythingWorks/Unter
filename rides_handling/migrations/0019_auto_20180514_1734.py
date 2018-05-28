# Generated by Django 2.0.4 on 2018-05-14 17:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rides_handling', '0018_auto_20180512_0937'),
    ]

    operations = [
        migrations.AddField(
            model_name='ride',
            name='estimated_trip_time',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=9),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ride',
            name='driver',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='driver', to='rides_handling.Profile'),
        ),
    ]
