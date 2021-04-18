from django import forms
from .models import Report
from .models import Firefighter


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ('stationid', 'reportid', 'departureTime', 'arrivalTime',
                  'actionEndTime', 'fireStationArrivalTime', 'incidentType',
                  'incidentPlace', 'sectionCommander', 'actionCommander',
                  'driver', 'perpetrator', 'victim', 'section', 'details',
                  'odometer', 'distance')


class FirefighterForm(forms.ModelForm):
    class Meta:
        model = Firefighter
        fields = ('firstName', 'lastName', 'stationid', 'isDriver', 'isSectionCommander', 'isActionCommander')


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegistrationForm(forms.Form):
    username = forms.CharField()
    firstName = forms.CharField()
    lastName = forms.CharField()
    email = forms.CharField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)
    passwordConfirmation = forms.CharField(widget=forms.PasswordInput)
class FirestationForm(forms.Form):
    stationName = forms.CharField(max_length=100)