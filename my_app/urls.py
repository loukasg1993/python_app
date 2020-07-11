from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name ='home'),
    path('view/', views.view_all, name='view'),
    path('view/delete/<int:personal_information_id>/', views.delete),
    path('add/', views.add_patient, name="add"),
    path('edit/<int:id>', views.editpost, name='editpost'),
    path('edit/', views.list, name='edit'),
    path('<int:personal_information_id>/delete/', views.delete2),
    path('appointment/<int:id>', views.make_appointment,name="appointment"),
    path('allappointments/', views.view_all_appointments, name='view_appointments'),
    path('allappointments/delete/<int:appointment_id>/', views.deleteapp),
    path('add_appointment/', views.addapp,name='addapp'),
    path('delete/<int:appointment_id>/', views.deleteapp),
    path('schedule/', views.schedule),
    path('showplots/', views.showplots),
    path('tomorrow_csv/', views.tomorrow_dose, name='export_csv'),
    path('year_csv/', views.lastyear, name='year_csv'),
    path('pdf/', views.tomorrowpdf, name='pdf'),
    path('yearpdf/', views.lastyearpdf, name='pdf'),




    ]