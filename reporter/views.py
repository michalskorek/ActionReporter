from io import StringIO

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Report, Firefighter, Firestation, FirestationMember
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .forms import ReportForm, LoginForm, RegistrationForm, FirefighterForm, FirestationForm, FirestatiomMemberForm

import datetime

@login_required
def create_firefighter(request):
    if request.method == "POST":
        form = FirefighterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            fireStation = Firestation.objects.filter(
                firestationmember=FirestationMember.objects.filter(memberid=request.user).first(),
                stationName=cd['stationid']).first()

            Firefighter.objects.create(stationid=fireStation, firstName=cd['firstName'], lastName=cd['lastName'],
                                       isDriver=cd['isDriver'], isSectionCommander=cd['isSectionCommander'],
                                       isActionCommander=cd['isActionCommander'])

            return render(request, "information.html",
                          {'message': "Pomyślnie dodano nowego strażaka", 'return_button': True})
    else:
        user = request.user
        form = FirefighterForm()
        form.fields['stationid'].queryset = Firestation.objects.filter(
            firestationmember=FirestationMember.objects.filter(memberid=user).first())

    return render(request, 'create_firefighter.html', {'form': form})

@login_required
def create_report_initial(request):
    user = request.user
    fireStations = Firestation.objects.filter(firestationmember=FirestationMember.objects.filter(memberid=user).first())
    return render(request, 'create_report_initial.html', {'fireStations': fireStations})

@login_required
def create_report(request, pk):
    fireStation = Firestation.objects.filter(stationid=pk).first()
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ReportForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            cd = form.cleaned_data
            section = ""
            for val in cd['section']:
                section += str(val) + ","
            section = section[:-1]
            Report.objects.create(
                stationid=fireStation.stationid,
                reportid=cd['reportid'],
                departureTime=cd['departureTime'],
                arrivalTime=cd['arrivalTime'],
                actionEndTime=cd['actionEndTime'],
                fireStationArrivalTime=cd['fireStationArrivalTime'],
                incidentType=cd['incidentType'],
                incidentPlace=cd['incidentPlace'],
                sectionCommander=cd['sectionCommander'],
                actionCommander=cd['actionCommander'],
                driver=cd['driver'],
                perpetrator=cd['perpetrator'],
                victim=cd['victim'],
                section=section,
                details=cd['details'],
                odometer=cd['odometer'],
                distance=cd['distance'],
                isLocked=False
            )
            return render(request, "information.html", {'message': "Pomyślnie dodano raport", 'return_button': True})

        # if a GET (or any other method) we'll create a blank form
    else:
        section = Firefighter.objects.filter(stationid=fireStation.stationid)
        sectionCommanders = section.filter(isSectionCommander=True)
        actionCommanders = section.filter(isActionCommander=True)
        drivers = section.filter(isDriver=True)
        lastReports = Report.objects.filter(stationid=pk)
        if not lastReports:
            lastId = 1
        else:
            lastId = int(lastReports.order_by('-reportid').first().reportid) + 1
        form = ReportForm(initial={'reportid': lastId})
        form.fields['driver'].queryset = drivers
        form.fields['section'].queryset = section
        form.fields['actionCommander'].queryset = actionCommanders
        form.fields['sectionCommander'].queryset = sectionCommanders

    return render(request, 'create_report.html', {'form': form, 'fireStation': fireStation})

@login_required
def modify_report(request, pk):
    report = get_object_or_404(Report, pk=pk)
    fireStation = Firestation.objects.filter(stationid=report.stationid).first()
    userStations = Firestation.objects.filter(
        firestationmember=FirestationMember.objects.filter(memberid=request.user).first())
    if fireStation not in userStations:
        return render(request, "information.html",
                      {'message': "Dostęp zabroniony", 'return_button': True})

    if request.method == "POST":
        form = ReportForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            cd = form.cleaned_data
            section = ""
            for val in cd['section']:
                section += str(val) + ","
            section = section[:-1]
            Report.objects.filter(pk=pk).update(
                stationid=fireStation.stationid,
                reportid=cd['reportid'],
                departureTime=cd['departureTime'],
                arrivalTime=cd['arrivalTime'],
                actionEndTime=cd['actionEndTime'],
                fireStationArrivalTime=cd['fireStationArrivalTime'],
                incidentType=cd['incidentType'],
                incidentPlace=cd['incidentPlace'],
                sectionCommander=str(cd['sectionCommander']),
                actionCommander=str(cd['actionCommander']),
                driver=str(cd['driver']),
                perpetrator=cd['perpetrator'],
                victim=cd['victim'],
                section=section,
                details=cd['details'],
                odometer=cd['odometer'],
                distance=cd['distance'],
                isLocked=False
            )
            return render(request, "information.html",
                          {'message': "Pomyślnie zmodyfikowano raport", 'return_button': True})
    else:
        section = Firefighter.objects.filter(stationid=fireStation.stationid)
        sectionCommanders = section.filter(isSectionCommander=True)
        actionCommanders = section.filter(isActionCommander=True)
        drivers = section.filter(isDriver=True)
        previousSection = report.section.split(",")
        selectedSection = []
        for firefighter in section:
            if str(firefighter) in previousSection:
                selectedSection.append(firefighter)

        form = ReportForm(initial={
            'reportid': report.reportid,
            'departureTime': report.departureTime,
            'arrivalTime': report.arrivalTime,
            'actionEndTime': report.actionEndTime,
            'fireStationArrivalTime': report.fireStationArrivalTime,
            'incidentType': report.incidentType,
            'incidentPlace': report.incidentPlace,
            'sectionCommander': sectionCommanders,
            'actionCommander': actionCommanders,
            'driver': drivers,
            'perpetrator': report.perpetrator,
            'victim': report.victim,
            'section': report.section,
            'details': report.details,
            'odometer': report.odometer,
            'distance': report.distance

        })
        form.fields['driver'].queryset = drivers
        form.fields['actionCommander'].queryset = actionCommanders
        form.fields['sectionCommander'].queryset = sectionCommanders
        form.fields['section'].queryset = section
    return render(request, 'modify_report.html', {'form': form, 'fireStation': fireStation, 'report': report,
                                                  'departureTime': report.departureTime.strftime("%Y-%m-%dT%H:%M"),
                                                  'arrivalTime': report.arrivalTime.strftime("%Y-%m-%dT%H:%M"),
                                                  'actionEndTime': report.actionEndTime.strftime("%Y-%m-%dT%H:%M"),
                                                  'fireStationArrivalTime': report.fireStationArrivalTime.strftime(
                                                      "%Y-%m-%dT%H:%M"),
                                                  'driver': report.driver})

@login_required
def reports_list(request):
    user = request.user
    stations = Firestation.objects.filter(firestationmember=FirestationMember.objects.filter(memberid=user).first())
    reports = Report.objects.filter(stationid__in=stations)
    return render(request, "reports.html", {'reports': reports})

@login_required
def report_details(request, pk):
    report = get_object_or_404(Report, pk=pk)
    userStations = Firestation.objects.filter(firestationmember=FirestationMember.objects.filter(memberid=request.user).first())
    station = Firestation.objects.filter(stationid=report.stationid).first()
    if station not in userStations:
        return render(request, "information.html",
                      {'message': "Dostęp zabroniony", 'return_button': True})
    firefighters = report.section.split(",")
    return render(request, 'report.html', {'report': report, 'firefighters': firefighters})
@login_required
def lock_report(request,pk):
    report = get_object_or_404(Report, pk=pk)
    userStations = Firestation.objects.filter(
        firestationmember=FirestationMember.objects.filter(memberid=request.user).first())
    station = Firestation.objects.filter(stationid=report.stationid).first()
    if station not in userStations:
        return render(request, "information.html",
                      {'message': "Dostęp zabroniony", 'return_button': True})
    Report.objects.filter(pk=pk).update(isLocked=True)
    return render(request, "information.html",
                  {'message': "Pomyślnie zamknięto raport", 'return_button': True})
def mainpage(request):
    return render(request, "index.html")

@login_required
def report_render_pdf_view(request, *args, **kwargs):
    pk = kwargs.get("pk")
    report = get_object_or_404(Report, pk=pk)
    template_path = "reportpdf.html"
    context = {'report': report}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    #  response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(html,
                                 dest=response, encoding='UTF-8', path="./reporter/templates/")
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, "information.html",
                                  {'message': "Zalogowano pomyślnie", 'return_button': True})
                else:
                    return render(request, "information.html",
                                  {'message': "Konto jest zablokowane", 'return_button': True})
            else:
                return render(request, "information.html",
                              {'message': "Nieprawidłowe dane logowania", 'return_button': True})
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return render(request, 'information.html', {'message': "Wylogowano pomyślnie", 'return_button': False})


def user_registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            exists = User.objects.filter(username=cd["username"]).exists()
            if exists:
                return render(request, "information.html", {'message': "Podany użytkownik już istnieje"})
            else:
                if cd["password"] == cd["passwordConfirmation"]:
                    User.objects.create_user(username=cd["username"], password=cd["password"],
                                             first_name=cd["firstName"], last_name=cd["lastName"],
                                             email=cd["email"])
                    return render(request, "information.html", {'message': "Zarejestrowano pomyślnie", })
                else:
                    return render(request, "information.html", {'message': "Hasła się nie zgadzają"})
    else:
        form = RegistrationForm()
        return render(request, "register.html", {'form': form})

@login_required
def profile(request):
    user = request.user
    fireStations = Firestation.objects.filter(
        stationid__in=FirestationMember.objects.filter(memberid=user).values("stationid"))
    firestationsEmpty = len(fireStations) == 0
    return render(request, "profile.html",
                  {"user": user, "fireStations": fireStations, "firestationsEmpty": firestationsEmpty})

@login_required
def create_firestation(request):
    if request.method == 'POST':
        form = FirestationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            newFirestation = Firestation.objects.create(stationName=cd["stationName"])
            FirestationMember.objects.create(stationid=newFirestation, memberid=request.user)
            return render(request, "information.html", {'message': "Pomyślnie stworzono remizę", 'return_button': True})
    else:
        form = FirestationForm()
        return render(request, "create_firestation.html", {'form': form})

@login_required
def firestation_details(request, pk):
    firestation = get_object_or_404(Firestation, pk=pk)
    firefighters = Firefighter.objects.filter(stationid=firestation)
    firestationMembers = User.objects.filter(
        id__in=FirestationMember.objects.filter(stationid=firestation).values("memberid"))
    if request.method == 'POST':
        form = FirestatiomMemberForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.filter(email=cd["userEmail"]).first()
            if user is not None:
                FirestationMember.objects.create(stationid=firestation, memberid=user)
                return render(request, "information.html",
                              {"message": "Pomyślnie dodano nowego moderatora", "return_button": True})
            return render(request, "information.html",
                          {"message": "Nie istnieje użytkownik o podanym adresie email", "return_button": True})
    return render(request, "firestation_details.html",
                  {"firestation": firestation, "firefighters": firefighters, "firestationMembers": firestationMembers})
