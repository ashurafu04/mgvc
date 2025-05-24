from django.shortcuts import render, get_object_or_404
from django.http import FileResponse, HttpResponse
from carnets.models import CarnetVoyage
from .models import Rapport
import os
from django.conf import settings

def generate_pdf_report(request, carnet_id):
    carnet = get_object_or_404(CarnetVoyage, id=carnet_id)
    rapport = carnet.generer_rapport(format="pdf")
    filepath = os.path.join(settings.MEDIA_ROOT, rapport.fichier_url.name)
    if os.path.exists(filepath):
        return FileResponse(open(filepath, 'rb'), as_attachment=True, filename=os.path.basename(filepath))
    return HttpResponse("PDF not found", status=404)

def generate_pie_chart(request, carnet_id):
    carnet = get_object_or_404(CarnetVoyage, id=carnet_id)
    rapport = carnet.generer_rapport(format="camembert")
    filepath = os.path.join(settings.MEDIA_ROOT, rapport.fichier_url.name)
    if os.path.exists(filepath):
        return FileResponse(open(filepath, 'rb'), content_type='image/png')
    return HttpResponse("Pie chart not found", status=404)

def view_report(request, carnet_id):
    carnet = get_object_or_404(CarnetVoyage, id=carnet_id)
    activites = carnet.activites_planifiees.select_related('activite__domaine')
    domaines = {}
    for ap in activites:
        domaine = ap.activite.domaine.nom
        domaines[domaine] = domaines.get(domaine, 0) + 1
    context = {
        'program': carnet,
        'total_activities': activites.count(),
        'total_hours': sum(ap.duree for ap in activites),
        'domaines': domaines,
        'carnet_id': carnet.id,
    }
    return render(request, 'carnets/report.html', context)
