from django.shortcuts import render, redirect, get_object_or_404
from .models import CarnetVoyage, ActivitePlanifiee, Activite
from comptes.models import Client
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse, HttpResponse, FileResponse
from activites.models import Activite, Domaine
from django.contrib import messages
from collections import defaultdict
from django.conf import settings
import os

def create_program_view (request):
    list(messages.get_messages(request))
    return render(request, 'carnets/create_program.html', {'step': 1})

def list_programs(request):
    return render(request, 'carnets/list_programs.html')

@login_required
def create_carnet(request):
    print(request.method)
    if request.method == 'POST':
        title = request.POST.get('titre')
        date_debut = request.POST.get('date_debut')
        date_fin = request.POST.get('date_fin')

        client = request.user.client  # suppose que l'utilisateur connecté est lié à un Client

        carnet = CarnetVoyage.objects.create(
            title = title,
            client=client,
            date_debut_sejour=date_debut,
            date_fin_sejour=date_fin,
        )
        return redirect('carnets:add_activity', carnet_id=carnet.id)  # redirige vers la liste après création

    return render(request, 'carnets/create_program.html')


@login_required
def add_activity(request, carnet_id):
    carnet = get_object_or_404(CarnetVoyage, id=carnet_id, client=request.user.client)

    if request.method == 'POST':
        activite_id = request.POST.get('activite')
        date_activite = request.POST.get('date_activite')
        heure_debut = request.POST.get('heure_debut')
        heure_fin = request.POST.get('heure_fin')
        note_memoire = request.POST.get('note_memoire')

        activite = get_object_or_404(Activite, id=activite_id)

        ActivitePlanifiee.objects.create(
            carnet_voyage=carnet,
            activite=activite,
            date_activite=date_activite,
            heure_debut=heure_debut,
            heure_fin=heure_fin,
            note_memoire=note_memoire,
            date_note=timezone.now() if note_memoire else None,
        )
        
        # Mettre à jour le coût total
        carnet.calculer_cout_total()
        messages.success(request, "Activité ajoutée avec succès.")
        return redirect('carnets:program_detail', carnet_id=carnet.id)

    domaines = Domaine.objects.filter(is_active=True)

    return render(request, 'carnets/planifier_activite.html', {
        'carnet': carnet,
        'domaines': domaines,
        'activites': [],
        'step': 2,
    })




def get_activites_par_domaine(request, domaine_id):
    activites = Activite.objects.filter(domaine_id=domaine_id, disponible=True)
    data = [{"id": a.id, "nom": a.nom} for a in activites]
    return JsonResponse(data, safe=False)


@login_required
def mes_programmes(request):
    client = request.user.client  # en supposant que Client est lié à User
    carnets = CarnetVoyage.objects.filter(client=client).prefetch_related('activites_planifiees__activite')

    return render(request, 'carnets/mes_programmes.html', {'carnets': carnets})

@login_required
def program_detail(request, carnet_id):
    carnet = get_object_or_404(CarnetVoyage, id=carnet_id, client=request.user.client)
    activites = carnet.activites_planifiees.all().select_related('activite')
    
    return render(request, 'carnets/program_detail.html', {
        'carnet': carnet,
        'activites': activites,
        'total_duration': carnet.duree_totale
    })

@login_required
def edit_activity(request, carnet_id, activity_id):
    carnet = get_object_or_404(CarnetVoyage, id=carnet_id, client=request.user.client)
    activity = get_object_or_404(ActivitePlanifiee, id=activity_id, carnet_voyage=carnet)
    
    if request.method == 'POST':
        date_activite = request.POST.get('date_activite')
        heure_debut = request.POST.get('heure_debut')
        heure_fin = request.POST.get('heure_fin')
        note_memoire = request.POST.get('note_memoire')
        
        activity.date_activite = date_activite
        activity.heure_debut = heure_debut
        activity.heure_fin = heure_fin
        if note_memoire:
            activity.modifier_note_memoire(note_memoire)
        activity.save()
        
        # Mettre à jour le coût total
        carnet.calculer_cout_total()
        
        return redirect('carnets:program_detail', carnet_id=carnet_id)
    
    return render(request, 'carnets/edit_activity.html', {
        'carnet': carnet,
        'activity': activity,
    })

@login_required
def generate_report(request, carnet_id):
    carnet = get_object_or_404(CarnetVoyage, id=carnet_id, client=request.user.client)
    activites = carnet.activites_planifiees.all().select_related('activite')
    
    # Prepare chart data
    activites_par_domaine = defaultdict(int)
    for activity in activites:
        activites_par_domaine[activity.activite.domaine.nom] += 1
    
    chart_data = {
        'labels': list(activites_par_domaine.keys()),
        'datasets': [{
            'data': list(activites_par_domaine.values()),
            'backgroundColor': [
                '#FF6384',
                '#36A2EB',
                '#FFCE56',
                '#4BC0C0',
                '#9966FF',
                '#FF9F40'
            ]
        }]
    }
    
    return render(request, 'carnets/report.html', {
        'carnet': carnet,
        'activites': activites,
        'total_duration': carnet.duree_totale,
        'chart_data': chart_data
    })

@login_required
def download_pdf(request, carnet_id):
    carnet = get_object_or_404(CarnetVoyage, id=carnet_id, client=request.user.client)
    rapport = carnet.generer_rapport(format="pdf")
    
    # Get the file path from the rapport's fichier_url
    if rapport.fichier_url:
        file_path = os.path.join(settings.MEDIA_ROOT, str(rapport.fichier_url))
        if os.path.exists(file_path):
            response = FileResponse(open(file_path, 'rb'), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="rapport_{carnet_id}.pdf"'
            return response
    
    return HttpResponse("Le PDF n'a pas pu être généré", status=500)
