from django.urls import path
from . import views

app_name = 'reporting'

urlpatterns = [
    path('rapport/pdf/<int:carnet_id>/', views.generate_pdf_report, name='generate_pdf_report'),
    path('rapport/camembert/<int:carnet_id>/', views.generate_pie_chart, name='generate_pie_chart'),
    path('rapport/visualiser/<int:carnet_id>/', views.view_report, name='view_report'),
]