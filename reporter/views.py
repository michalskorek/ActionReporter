from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Report, Firefighter, Firestation, FirestationMember
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .forms import ReportForm, LoginForm, RegistrationForm, FirefighterForm, FirestationForm, FirestatiomMemberForm


def getUserFirestationByName(user, name):
    return Firestation.objects.filter(
        stationid__in=FirestationMember.objects.filter(memberid=user).values("stationid")).filter(
        stationName=name).first()


def getUserFirestations(user):
    return Firestation.objects.filter(
        stationid__in=FirestationMember.objects.filter(memberid=user).values("stationid"))


def getFirestation(id):
    return Firestation.objects.filter(stationid=id).first()


def getFirestationSection(station):
    return Firefighter.objects.filter(stationid=station)


def getFirestationReports(station):
    return Report.objects.filter(stationid=station)


def getReport(id):
    return get_object_or_404(Report, pk=id)


def lockReport(id):
    Report.objects.filter(pk=id).update(isLocked=True)


def getFirestationMembers(station):
    return User.objects.filter(
        id__in=FirestationMember.objects.filter(stationid=station).values("memberid"))


@login_required
def create_firefighter(request):
    if request.method == "POST":
        form = FirefighterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            fireStation = getUserFirestationByName(request.user, cd['stationid'])
            Firefighter.objects.create(stationid=fireStation, firstName=cd['firstName'], lastName=cd['lastName'],
                                       isDriver=cd['isDriver'], isSectionCommander=cd['isSectionCommander'],
                                       isActionCommander=cd['isActionCommander'])
            return render(request, "information.html",
                          {'message': "Pomy??lnie dodano nowego stra??aka", 'return_button': True})
    else:
        form = FirefighterForm()
        form.fields['stationid'].queryset = getUserFirestations(request.user)

    return render(request, 'create_firefighter.html', {'form': form})


@login_required
def create_report_initial(request):
    fireStations = getUserFirestations(request.user)
    return render(request, 'create_report_initial.html', {'fireStations': fireStations})


@login_required
def create_report(request, pk):
    firestation = getFirestation(pk)
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
                stationid=firestation.stationid,
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
            return render(request, "information.html", {'message': "Pomy??lnie dodano raport", 'return_button': True})

        # if a GET (or any other method) we'll create a blank form
    else:
        section = getFirestationSection(firestation.stationid)
        sectionCommanders = section.filter(isSectionCommander=True)
        actionCommanders = section.filter(isActionCommander=True)
        drivers = section.filter(isDriver=True)
        lastReports = getFirestationReports(pk)
        if not lastReports:
            lastId = 1
        else:
            lastId = int(lastReports.order_by('-reportid').first().reportid) + 1
        form = ReportForm(initial={'reportid': lastId})
        form.fields['driver'].queryset = drivers
        form.fields['section'].queryset = section
        form.fields['actionCommander'].queryset = actionCommanders
        form.fields['sectionCommander'].queryset = sectionCommanders

    return render(request, 'create_report.html', {'form': form, 'fireStation': firestation})


@login_required
def modify_report(request, pk):
    report = getReport(pk)
    firestation = getFirestation(report.stationid)
    firestations = getUserFirestations(request.user)
    if firestation not in firestations:
        return render(request, "information.html",
                      {'message': "Dost??p zabroniony", 'return_button': True})

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
                stationid=firestation.stationid,
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
                          {'message': "Pomy??lnie zmodyfikowano raport", 'return_button': True})
    else:
        section = getFirestationSection(firestation.stationid)
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
            'distance': int(report.distance)

        })
        form.fields['driver'].queryset = drivers
        form.fields['actionCommander'].queryset = actionCommanders
        form.fields['sectionCommander'].queryset = sectionCommanders
        form.fields['section'].queryset = section
    return render(request, 'modify_report.html', {'form': form, 'fireStation': firestation, 'report': report,
                                                  'departureTime': report.departureTime.strftime("%Y-%m-%dT%H:%M"),
                                                  'arrivalTime': report.arrivalTime.strftime("%Y-%m-%dT%H:%M"),
                                                  'actionEndTime': report.actionEndTime.strftime("%Y-%m-%dT%H:%M"),
                                                  'fireStationArrivalTime': report.fireStationArrivalTime.strftime(
                                                      "%Y-%m-%dT%H:%M"),
                                                  'driver': report.driver,
                                                  'sectionCommander': report.sectionCommander,
                                                  'actionCommander': report.actionCommander,
                                                  'section': report.section})


@login_required
def reports_list(request):
    user = request.user
    firestations = getUserFirestations(request.user)
    reports = Report.objects.filter(stationid__in=firestations)
    return render(request, "reports.html", {'reports': reports})


@login_required
def report_details(request, pk):
    report = getReport(pk)
    firestations = getUserFirestations(request.user)
    station = getFirestation(report.stationid)
    if station not in firestations:
        return render(request, "information.html",
                      {'message': "Dost??p zabroniony", 'return_button': True})
    firefighters = report.section.split(",")
    return render(request, 'report.html', {'report': report, 'firefighters': firefighters})


@login_required
def lock_report(request, pk):
    report = getReport(pk)
    firestations = getUserFirestations(request.user)
    station = getFirestation(report.reportid)
    if station not in firestations:
        return render(request, "information.html",
                      {'message': "Dost??p zabroniony", 'return_button': True})
    lockReport(pk)
    return render(request, "information.html",
                  {'message': "Pomy??lnie zamkni??to raport", 'return_button': True})


def mainpage(request):
    return render(request, "index.html")


@login_required
def report_render_pdf_view(request, *args, **kwargs):
    pk = kwargs.get("pk")
    report = getReport(pk)
    # report = get_object_or_404(Report, pk=pk)
    template_path = "reportpdf.html"
    context = {'report': report, 'section': report.section.split(",")}
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
    if request.user.is_authenticated:
        return mainpage(request)
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
                                  {'message': "Zalogowano pomy??lnie", 'return_button': True})
                else:
                    return render(request, "information.html",
                                  {'message': "Konto jest zablokowane", 'return_button': True})
            else:
                return render(request, "information.html",
                              {'message': "Nieprawid??owe dane logowania", 'return_button': True})
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return render(request, 'information.html', {'message': "Wylogowano pomy??lnie", 'return_button': False})


def user_registration(request):
    if request.user.is_authenticated:
        return mainpage(request)
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            exists = User.objects.filter(username=cd["username"]).exists()
            if exists:
                return render(request, "information.html", {'message': "Podany u??ytkownik ju?? istnieje"})
            else:
                if cd["password"] == cd["passwordConfirmation"]:
                    User.objects.create_user(username=cd["username"], password=cd["password"],
                                             first_name=cd["firstName"], last_name=cd["lastName"],
                                             email=cd["email"])
                    return render(request, "information.html", {'message': "Zarejestrowano pomy??lnie", })
                else:
                    return render(request, "information.html", {'message': "Has??a si?? nie zgadzaj??"})
    else:
        form = RegistrationForm()
        return render(request, "register.html", {'form': form})


@login_required
def profile(request):
    user = request.user
    firestations = getUserFirestations(request.user)
    firestationsEmpty = len(firestations) == 0
    return render(request, "profile.html",
                  {"user": user, "fireStations": firestations, "firestationsEmpty": firestationsEmpty})


@login_required
def create_firestation(request):
    if request.method == 'POST':
        form = FirestationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            newFirestation = Firestation.objects.create(stationName=cd["stationName"])
            FirestationMember.objects.create(stationid=newFirestation, memberid=request.user)
            return render(request, "information.html", {'message': "Pomy??lnie stworzono remiz??", 'return_button': True})
    else:
        form = FirestationForm()
        return render(request, "create_firestation.html", {'form': form})


@login_required
def firestation_details(request, pk):
    firestation = getFirestation(pk)
    firefighters = getFirestationSection(firestation)
    firestationMembers = getFirestationMembers(firestation)


    if request.method == 'POST':
        form = FirestatiomMemberForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.filter(email=cd["userEmail"]).first()
            if user is not None:
                FirestationMember.objects.create(stationid=firestation, memberid=user)
                return render(request, "information.html",
                              {"message": "Pomy??lnie dodano nowego moderatora", "return_button": True})
            return render(request, "information.html",
                          {"message": "Nie istnieje u??ytkownik o podanym adresie email", "return_button": True})
    return render(request, "firestation_details.html",
                  {"firestation": firestation, "firefighters": firefighters, "firestationMembers": firestationMembers})


@login_required
def delete_firefighter(request, pk):
    Firefighter.objects.get(pk=pk).delete()
    return render(request, "information.html",
                  {'message': "Pomy??lnie usuni??to stra??aka z remizy", 'return_button': True})
