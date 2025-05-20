from django.urls import path
from . import views

app_name = 'carnets'

urlpatterns = [
    path('', views.list_programs, name='list_programs'),
    path('create/', views.create_program, name='create_program'),
    path('<int:program_id>/', views.program_detail, name='program_detail'),
    path('<int:program_id>/activity/add/', views.add_activity, name='add_activity'),
    path('<int:program_id>/activity/<int:activity_id>/edit/', views.edit_activity, name='edit_activity'),
    path('<int:program_id>/report/', views.generate_report, name='generate_report'),
    path('<int:program_id>/report/pdf/', views.download_pdf, name='download_pdf'),
]