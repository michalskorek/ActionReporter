from io import StringIO

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Report, Firefighter, Firestation
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .forms import ReportForm, LoginForm, RegistrationForm, FirefighterForm, FirestationForm

import datetime


def create_firefighter(request):
    if request.method == "POST":
        form = FirefighterForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.author = request.user
            report.published_date = datetime.datetime.now()
            report.save()
    else:
        form = FirefighterForm()

    return render(request, 'create_firefighter.html', {'form': form})


def create_report(request):
    drivers = Firefighter.objects.filter(isDriver=True)
    sectionCommanders = Firefighter.objects.filter(isSectionCommander=True)
    actionCommanders = Firefighter.objects.filter(isActionCommander=True)
    if request.method == "POST":
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.author = request.user
            report.published_date = datetime.datetime.now()
            report.save()
    else:
        form = ReportForm()

    return render(request, 'create_report.html',
                  {'form': form, 'drivers': drivers, 'sectionCommanders': sectionCommanders,
                   'actionCommanders': actionCommanders})


def modify_report(request, pk):
    report = get_object_or_404(Report, pk=pk)
    drivers = Firefighter.objects.filter(isDriver=True)
    sectionCommanders = Firefighter.objects.filter(isSectionCommander=True)
    actionCommanders = Firefighter.objects.filter(isActionCommander=True)
    if request.method == "POST":
        form = ReportForm(request.POST, instance=report)
        if form.is_valid():
            report = form.save(commit=False)
            report.author = request.user
            report.published_date = datetime.datetime.now()
            report.save()
    else:
        form = ReportForm(instance=report)
    return render(request, 'create_report.html',
                  {'form': form, 'drivers': drivers, 'sectionCommanders': sectionCommanders,
                   'actionCommanders': actionCommanders})


def reports_list(request):
    reports = Report.objects.all()
    return render(request, "reports.html", {'reports': reports})


def report_details(request, pk):
    report = get_object_or_404(Report, pk=pk)
    firefighters = report.section.split(",")
    return render(request, 'report.html', {'report': report, 'firefighters': firefighters})


def mainpage(request):
    authenticated = request.user.is_authenticated
    return render(request, "index.html")


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
         dest=response, encoding='UTF-8')
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


def profile(request):
    user = request.user
    fireStations = Firestation.objects.filter(ownerid=user.id)
    firestationsEmpty = len(fireStations) == 0
    return render(request, "profile.html", {"user": user, "fireStations": fireStations, "firestationsEmpty":firestationsEmpty})

def create_firestation(request):
    if request.method == 'POST':
        form = FirestationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            Firestation.objects.create(ownerid=request.user, stationName=cd["stationName"])
            return render(request, "information.html", {'message': "Pomyślnie stworzono remizę", 'return_button':True})
    else:
        form = FirestationForm()
        return render(request, "create_firestation.html", {'form': form})
def firestation_details(request,pk):
    firestation = get_object_or_404(Firestation, pk=pk)
    firefighters = Firefighter.objects.filter(stationid=firestation)
    return render(request, "firestation_details.html", {"firestation":firestation, "firefighters":firefighters})