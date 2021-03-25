from django.urls import path
from . import views

urlpatterns = [
    path('', views.mainpage,name='index'),
    path('reports/', views.reports_list, name='reports'),
    path('pdf/<pk>/',views.report_render_pdf_view, name='render-to-pdf')
]
