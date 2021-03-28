from django import forms
from .models import Report


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ('stationid', 'reportid', 'departureTime', 'arrivalTime',
                  'actionEndTime', 'fireStationArrivalTime', 'incidentType',
                  'incidentPlace', 'sectionCommander', 'actionCommander',
                  'driver', 'perpetrator', 'victim', 'section', 'details',
                  'counter', 'distance')
