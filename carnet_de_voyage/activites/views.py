from django.shortcuts import render
from .models import Domaine

def list_programs_view(request):
    domaines = Domaine.objects.prefetch_related('activites').all()
    return render(request, 'carnets/list_programs.html', {'domaines': domaines})
