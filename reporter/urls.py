from django.urls import path
from . import views

urlpatterns = [
    path('', views.mainpage,name='index'),
    path('reports/', views.reports_list, name='reports'),
    path('create-report/',views.create_report, name='create-report'),
    path('reports/<pk>', views.report_details, name="report-details"),
    path('reports/<pk>/edit/', views.modify_report, name='modify-report'),
    path('pdf/<pk>/',views.report_render_pdf_view, name='render-to-pdf')
]
