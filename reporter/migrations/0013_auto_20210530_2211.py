# Generated by Django 3.1.7 on 2021-05-30 20:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reporter', '0012_auto_20210530_2158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='firefighter',
            name='firstName',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='firefighter',
            name='lastName',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='firestation',
            name='stationName',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='report',
            name='actionEndTime',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 30, 22, 11, 14, 687065)),
        ),
        migrations.AlterField(
            model_name='report',
            name='arrivalTime',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 30, 22, 11, 14, 687065)),
        ),
        migrations.AlterField(
            model_name='report',
            name='departureTime',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 30, 22, 11, 14, 687065)),
        ),
        migrations.AlterField(
            model_name='report',
            name='fireStationArrivalTime',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 30, 22, 11, 14, 687065)),
        ),
    ]
