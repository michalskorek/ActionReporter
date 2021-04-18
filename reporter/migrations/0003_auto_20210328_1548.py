# Generated by Django 3.1.7 on 2021-03-28 13:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reporter', '0002_auto_20210328_1547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='actionEndTime',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 28, 15, 48, 18, 832393)),
        ),
        migrations.AlterField(
            model_name='report',
            name='arrivalTime',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 28, 15, 48, 18, 832393)),
        ),
        migrations.AlterField(
            model_name='report',
            name='departureTime',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 28, 15, 48, 18, 832393)),
        ),
        migrations.AlterField(
            model_name='report',
            name='fireStationArrivalTime',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 28, 15, 48, 18, 832393)),
        ),
        migrations.AlterField(
            model_name='report',
            name='privateid',
            field=models.CharField(default='', max_length=10),
        ),
    ]
