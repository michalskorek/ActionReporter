from django.urls import path
from . import views

urlpatterns = [
    path('', views.mainpage,name='index'),
    path('reports/', views.reports_list, name='reports'),
    path('create-report/', views.create_report_initial, name='create-report-initial'),
    path('create-report/<pk>',views.create_report, name='create-report'),
    path('create-firefighter/',views.create_firefighter, name='create-firefighter'),
    path('reports/<pk>', views.report_details, name="report-details"),
    path('reports/<pk>/edit/', views.modify_report, name='modify-report'),
    path('pdf/<pk>/',views.report_render_pdf_view, name='render-to-pdf'),
    path('login/', views.user_login, name='login'),
    path('register/',views.user_registration, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('create-firestation/',views.create_firestation,name='create-firestation'),
    path('firestations/<pk>', views.firestation_details, name="firestation-details")
]
