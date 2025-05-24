from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'carnets'

urlpatterns = [
    path('', views.list_programs, name='list_programs'),
    path('create/', views.create_program_view, name='create_program'),
    path('creer/', views.create_carnet, name='create_carnet'),
    path('get_activites/<int:domaine_id>/', views.get_activites_par_domaine, name='get_activites_par_domaine'),
    path('mes-programmes/', views.mes_programmes, name='mes_programmes'),
    path('<int:carnet_id>/', views.program_detail, name='program_detail'),
    path('<int:carnet_id>/activity/add/', views.add_activity, name='add_activity'),
    path('<int:carnet_id>/activity/<int:activity_id>/edit/', views.edit_activity, name='edit_activity'),
    path('<int:carnet_id>/report/', views.generate_report, name='generate_report'),
    path('<int:carnet_id>/report/pdf/', views.download_pdf, name='download_pdf'),
    path('<int:carnet_id>/delete/', views.delete_carnet, name='delete_carnet'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)