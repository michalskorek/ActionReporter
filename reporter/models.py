from django.db import models
from django.forms import ModelForm
from django.utils import timezone


class Report(models.Model):
    id = models.CharField(max_length=10,primary_key=True)
    departureTime = models.DateTimeField()
    arrivalTime = models.DateTimeField()
    actionEndTime = models.DateTimeField()
    fireStationArrivalTime = models.DateTimeField()
    incidentType = models.CharField(max_length=1000)
    incidentPlace = models.CharField(max_length=20)
    sectionCommander = models.CharField(max_length=10)
    actionCommander = models.CharField(max_length=10)
    driver = models.CharField(max_length=10)
    perpetrator = models.CharField(max_length=1000)
    victim = models.CharField(max_length=1000)
    details = models.CharField(max_length=2000)
    counter = models.CharField(max_length=10)
    distance = models.CharField(max_length=10)

    def __str__(self):
        return str(self.id)


