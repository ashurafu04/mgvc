from . import views
from django.urls import path

app_name = 'admin_custom'

urlpatterns = [
    path('domains/', views.manage_domains, name='manage_domains'),
    path('domains/add/', views.add_domain, name='admin_add_domain'),
    path('domains/edit/<int:domain_id>/', views.edit_domain, name='admin_edit_domain'),
    path('domains/delete/<int:domain_id>/', views.delete_domain, name='admin_delete_domain'),
    path('activities/', views.manage_activities, name='manage_activities'),
    path('activities/add/', views.add_activity, name='admin_add_activity'),
    path('activities/delete/<int:id>/', views.delete_activity, name='admin_delete_activity'),
    path('activities/edit/<int:id>/', views.edit_activity, name='admin_edit_activity'),
    path('travel_report/', views.travel_report, name='travel_report'),
]