# Generated by Django 3.1.7 on 2021-04-18 11:26

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reporter', '0008_auto_20210417_1846'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='actionEndTime',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 18, 13, 26, 23, 144225)),
        ),
        migrations.AlterField(
            model_name='report',
            name='arrivalTime',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 18, 13, 26, 23, 144225)),
        ),
        migrations.AlterField(
            model_name='report',
            name='departureTime',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 18, 13, 26, 23, 144225)),
        ),
        migrations.AlterField(
            model_name='report',
            name='fireStationArrivalTime',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 18, 13, 26, 23, 144225)),
        ),
        migrations.CreateModel(
            name='Firestation',
            fields=[
                ('stationid', models.AutoField(primary_key=True, serialize=False)),
                ('stationName', models.CharField(default='', max_length=100)),
                ('ownerid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='firefighter',
            name='stationid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reporter.firestation'),
        ),
    ]
