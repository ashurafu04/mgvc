from django.shortcuts import render, redirect, get_object_or_404
from .models import CarnetVoyage, ActivitePlanifiee, Activite
from comptes.models import Client
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse
from activites.models import Activite, Domaine

def create_program_view (request):
    return render(request, 'carnets/create_program.html', {'step': 1})

def list_programs(request):
    return render(request, 'carnets/list_programs.html')

@login_required
def create_carnet(request):
    print(request.method)
    if request.method == 'POST':
        date_debut = request.POST.get('date_debut')
        date_fin = request.POST.get('date_fin')

        client = request.user.client  # suppose que l'utilisateur connecté est lié à un Client

        carnet = CarnetVoyage.objects.create(
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
        return redirect('carnets:add_activity', carnet_id=carnet.id)

    domaines = Domaine.objects.filter(is_active=True)

    return render(request, 'carnets/planifier_activite.html', {
        'carnet': carnet,
        'domaines': domaines,
        'activites': [],  # inutile ici car activites seront chargées via JS en fonction du domaine choisi
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
