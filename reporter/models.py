import datetime

from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
from django.utils import timezone


class Firestation(models.Model):
    stationid = models.AutoField(primary_key=True)
    stationName = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.stationName


class Firefighter(models.Model):
    id = models.AutoField(primary_key=True)
    firstName = models.CharField(max_length=25, default="")
    lastName = models.CharField(max_length=25, default="")
    stationid = models.ForeignKey(Firestation, on_delete=models.CASCADE)
    isDriver = models.BooleanField(default=False)
    isSectionCommander = models.BooleanField(default=False)
    isActionCommander = models.BooleanField(default=False)

    def __str__(self):
        return self.firstName + " " + self.lastName


class Report(models.Model):
    id = models.AutoField(primary_key=True)
    stationid = models.TextField(default="")
    reportid = models.TextField(default="")
    departureTime = models.DateTimeField(default=datetime.datetime.now())
    arrivalTime = models.DateTimeField(default=datetime.datetime.now())
    actionEndTime = models.DateTimeField(default=datetime.datetime.now())
    fireStationArrivalTime = models.DateTimeField(default=datetime.datetime.now())
    incidentType = models.TextField(default="")
    incidentPlace = models.TextField(default="")
    sectionCommander = models.TextField(default="")
    actionCommander = models.TextField(default="")
    driver = models.TextField(default="")
    perpetrator = models.TextField(default="")
    victim = models.TextField(default="")
    section = models.TextField(default="")
    details = models.TextField(default="")
    odometer = models.TextField(default="")
    distance = models.TextField(default="")
    isLocked = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class FirestationMember(models.Model):
    id = models.AutoField(primary_key=True)
    stationid = models.ForeignKey(Firestation, on_delete=models.CASCADE)
    memberid = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self)
