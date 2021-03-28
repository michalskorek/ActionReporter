from .models import Report
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .forms import ReportForm
from django.contrib import messages
import datetime


def create_report(request):
    if request.method == "POST":
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.author = request.user
            report.published_date = datetime.datetime.now()
            report.save()
    else:
        form = ReportForm()

    return render(request, 'create_report.html', {'form': form})


def reports_list(request):
    reports = Report.objects.all()
    return render(request, "reports.html", {'reports': reports})


def mainpage(request):
    return render(request, "index.html")


def report_render_pdf_view(request, *args, **kwargs):
    pk = kwargs.get("pk")
    report = Report.objects.get(pk=pk)
    template_path = "report.html"
    context = {'report': report}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    #  response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def render_pdf_view(request):
    pass
