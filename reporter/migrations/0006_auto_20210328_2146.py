# Generated by Django 3.1.7 on 2021-03-28 19:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reporter', '0005_auto_20210328_1712'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='isLocked',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='report',
            name='actionEndTime',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 28, 21, 46, 37, 449718)),
        ),
        migrations.AlterField(
            model_name='report',
            name='arrivalTime',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 28, 21, 46, 37, 449718)),
        ),
        migrations.AlterField(
            model_name='report',
            name='departureTime',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 28, 21, 46, 37, 449718)),
        ),
        migrations.AlterField(
            model_name='report',
            name='fireStationArrivalTime',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 28, 21, 46, 37, 449718)),
        ),
    ]
