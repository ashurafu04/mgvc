from django.urls import path
from .views import list_programs_view

urlpatterns = [
    path('list-programs/', list_programs_view, name='list_programs'),
]
