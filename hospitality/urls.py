"""anomalyes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home),
    path('index/', views.index),
    path('', views.index, name='index'),
    path('contact/', views.contact),
    
    # Auth System
    path('register/', views.register),
    path('addregister/', views.addregister),
    path('login/', views.login),
    path('addlogin/', views.addlogin),
    path('logout/', views.logout),
    
    # Doctors & Users Hub
    path('doctor/', views.doctor),
    path('adddoctor/', views.adddoctor),
    path('viewdoctor/', views.viewdoctor),
    path('viewuser/', views.viewuser),
    
    # Medical Intelligence Engine
    path('predict/', views.predict),
    path('predict_disease/', views.predict_disease),
    path('history/', views.view_history),
    path('prescriptions/', views.view_prescriptions),
    
    # Communications Matrix
    path('chatbot/', views.chatbot),
    path('chatbot_query/', views.chatbot_query),
    path('feedback/', views.send_feedback),
    path('view_feedback/', views.view_feedback),
    path('respond_feedback/', views.admin_respond_feedback),
    path('add_review/', views.add_review),
    
    # Appointments & Slot Management
    path('book_appointment/', views.book_appointment),
    path('confirm_booking/', views.confirm_booking),
    path('appointments/', views.appointments),
    path('update_status/', views.update_appointment_status),
    path('add_slot/', views.add_slot),
    path('view_slots/', views.view_slots),
    path('book_slot/', views.book_slot),
    
    # Reports Matrix
    path('log_report/<int:patient_id>/', views.log_report, name='log_report'),
    path('patient_history/<int:patient_id>/', views.doctor_view_patient_history, name='doctor_patient_history'),
    path('cancel_appointment/', views.cancel_appointment, name='cancel_appointment'),
    path('add_report/', views.add_report, name='add_report'),
    path('view_reports/', views.view_reports, name='view_reports'),
    path('profile/', views.profile, name='profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
