import datetime

from django.db import models
from django.forms import ModelForm
from django.utils import timezone


class Report(models.Model):
    id = models.AutoField(primary_key=True)
    stationid = models.CharField(max_length=10, default="")
    reportid = models.CharField(max_length=10, default="")
    departureTime = models.DateTimeField(default=datetime.datetime.now())
    arrivalTime = models.DateTimeField(default=datetime.datetime.now())
    actionEndTime = models.DateTimeField(default=datetime.datetime.now())
    fireStationArrivalTime = models.DateTimeField(default=datetime.datetime.now())
    incidentType = models.CharField(max_length=1000, default="")
    incidentPlace = models.CharField(max_length=50, default="")
    sectionCommander = models.CharField(max_length=50, default="")
    actionCommander = models.CharField(max_length=50, default="")
    driver = models.CharField(max_length=50, default="")
    perpetrator = models.CharField(max_length=1000, default="")
    victim = models.CharField(max_length=1000, default="")
    section = models.CharField(max_length=1000, default="")
    details = models.CharField(max_length=2000, default="")
    counter = models.CharField(max_length=10, default="")
    distance = models.CharField(max_length=10, default="")
    isLocked = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)
