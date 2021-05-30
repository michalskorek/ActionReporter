from django import forms

from .models import Firefighter
from .models import Firestation


class ReportForm(forms.Form):
    reportid = forms.IntegerField(label="ID raportu", required=True)
    departureTime = forms.DateTimeField(label="Czas wyjazdu z remizy",
                                        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}), required=True)
    arrivalTime = forms.DateTimeField(label="Czas przyjazdu na miejsce", widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}), required=True)
    actionEndTime = forms.DateTimeField(label="Czas zakończenia akcji", widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),required=True)
    fireStationArrivalTime = forms.DateTimeField(label="Czas powrotu do remizy", widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),required=True)
    incidentType = forms.CharField(label="Typ zdarzenia", required=True)
    incidentPlace = forms.CharField(label="Miejsce zdarzenia", required=True)
    sectionCommander = forms.ModelChoiceField(label="Dowódca sekcji",
                                              queryset=Firefighter.objects.filter(isSectionCommander=True), required=True)
    actionCommander = forms.ModelChoiceField(label="Dowódca akcji",
                                             queryset=Firefighter.objects.filter(isActionCommander=True), required=True)
    driver = forms.ModelChoiceField(label = "Kierowca",queryset=Firefighter.objects.filter(isDriver=True), required=True)
    perpetrator = forms.CharField(label="Sprawca zdarzenia", required=True)
    victim = forms.CharField(label="Poszkodowany", required=True)
    section = forms.ModelMultipleChoiceField(label="Sekcja", widget=forms.CheckboxSelectMultiple,
                                             queryset=Firefighter.objects.all(), required=True)
    details = forms.CharField(label="Szczegóły zdarzenia", required=True)
    odometer = forms.IntegerField(label="Stan licznika",required=True)
    distance = forms.IntegerField(label="Odległość od miejsca zdarzenia", required=True)


class FirefighterForm(forms.Form):
    firstName = forms.CharField(label="Imie")
    lastName = forms.CharField(label="Nazwisko")
    stationid = forms.ModelChoiceField(queryset=Firestation.objects.all(), label="Remiza")
    isDriver = forms.BooleanField(label="Jest kierowcą",initial=False, required=False)
    isSectionCommander = forms.BooleanField(label="Jest dowódcą sekcji", initial=False, required=False)
    isActionCommander = forms.BooleanField(label="Jest dowódcą akcji", initial=False, required=False)

class LoginForm(forms.Form):
    username = forms.CharField(label="Nazwa użytkownika")
    password = forms.CharField(widget=forms.PasswordInput, label="Hasło")


class RegistrationForm(forms.Form):
    username = forms.CharField(label="Nazwa użytkownika")
    firstName = forms.CharField(label="Imie")
    lastName = forms.CharField(label="Nazwisko")
    email = forms.CharField(widget=forms.EmailInput, label="Adres email")
    password = forms.CharField(widget=forms.PasswordInput, label="Hasło")
    passwordConfirmation = forms.CharField(widget=forms.PasswordInput, label="Potwierdź hasło")


class FirestationForm(forms.Form):
    stationName = forms.CharField(label="Nazwa remizy")


class FirestatiomMemberForm(forms.Form):
    userEmail = forms.CharField(widget=forms.EmailInput)
