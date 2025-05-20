from django.urls import path
from . import views

app_name = 'admin_custom'

urlpatterns = [
    path('domains/', views.manage_domains, name='admin_domains'),
    path('domains/add/', views.add_domain, name='admin_add_domain'),
    path('activities/', views.manage_activities, name='admin_activities'),
    path('activities/add/', views.add_activity, name='admin_add_activity'),
]