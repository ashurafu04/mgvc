from django.urls import path
from . import views

app_name = 'admin_custom'

urlpatterns = [
    path('domains/', views.manage_domains, name='admin_domains'),
    path('domains/add/', views.add_domain, name='admin_add_domain'),
    path('activities/', views.manage_activities, name='admin_activities'),
    path('activities/add/', views.add_activity, name='admin_add_activity'),
    path('travel_programs/', views.view_travel_programs, name='view_travel_programs'),
    path('travel_programs/create/', views.create_travel_program, name='create_travel_program'),
    path('travel_programs/<int:id>/', views.travel_program_detail, name='program_detail'),
    path('activities/edit/<int:id>/', views.edit_activity, name='edit_activity'),
    path('travel_report/', views.travel_report, name='travel_report'),
]