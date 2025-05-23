from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from activites.models import Domaine
from comptes.models import Administrateur
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from activites.models import Domaine
from activites.models import Activite
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

def is_admin(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(is_admin)
def manage_domains(request):
    domaines = Domaine.objects.all()
    return render(request, 'admin/domains.html', {
        'domains': domaines
    })

@user_passes_test(is_admin)
def add_domain(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        description = request.POST.get('description', '')
        admin = Administrateur.objects.filter(pk=request.user.pk).first()
        if nom:
            Domaine.objects.create(nom=nom, description=description, gestionnaire=admin)
        return redirect('admin_custom:manage_domains')
    return redirect('admin_custom:admin_domains')

@user_passes_test(is_admin)
@login_required
def manage_activities(request):
    activities = Activite.objects.select_related('domaine', 'gestionnaire').all()
    domains = Domaine.objects.all()
    return render(request, 'admin/activities.html', {'activities': activities, 'domains': domains})

@user_passes_test(is_admin)
def add_activity(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        domaine_id = request.POST.get('domaine_id')
        capacite = request.POST.get('capacite')
        cout = request.POST.get('cout')
        duree = request.POST.get('duree')
        description = request.POST.get('description', '')
        admin = Administrateur.objects.filter(pk=request.user.pk).first()
        domaine = Domaine.objects.filter(pk=domaine_id).first()
        if nom and domaine and capacite and cout and duree:
            Activite.objects.create(
                nom=nom,
                domaine=domaine,
                capacite_max=capacite,
                cout=cout,
                duree=duree,
                description=description,
                gestionnaire=admin
            )
        return redirect('admin_custom:manage_activities')
    return redirect('admin_custom:manage_activities')


def view_travel_programs(request):
    travel_programs = []  # Fetch travel programs from the database
    return render(request, 'view_travel_programs.html', {'travel_programs': travel_programs})

def create_travel_program(request):
    if request.method == 'POST':
        # Handle form submission
        return redirect('admin_custom:view_travel_programs')
    return render(request, 'create_travel_program.html')

def travel_program_detail(request, id):
    travel_program = None  # Fetch the travel program by id
    return redirect('admin_manage_travel_programs')

@user_passes_test(is_admin)
def edit_activity(request, id):
    activity = get_object_or_404(Activite, id=id)
    if request.method == 'POST':
        activity.nom = request.POST.get('nom')
        activity.description = request.POST.get('description')
        domaine_id = request.POST.get('domaine_id')
        if domaine_id:
            activity.domaine = Domaine.objects.get(id=domaine_id)
        activity.save()
        messages.success(request, 'Activity updated successfully.')
        return redirect('admin_custom:manage_activities')
    return render(request, 'carnets/edit_activity.html', {'activity': activity})

def travel_report(request):
    report_url = ""  # Generate or fetch the report URL
    return render(request, 'travel_report.html', {'report_url': report_url})


@login_required
def edit_domain(request, domain_id):
    domain = get_object_or_404(Domaine, id=domain_id)
    if request.method == 'POST':
        nom = request.POST.get('nom')
        description = request.POST.get('description')
        if nom:
            domain.nom = nom
        if description:
            domain.description = description
        domain.save()
        messages.success(request, 'Domain updated successfully.')
        return redirect(reverse('admin_custom:manage_domains'))
    return redirect(reverse('admin_custom:manage_domains'))

@login_required
def delete_domain(request, domain_id):
    domain = get_object_or_404(Domaine, id=domain_id)
    if request.method == 'POST':
        domain.delete()
        messages.success(request, 'Domain deleted successfully.')
        return redirect(reverse('admin_custom:manage_domains'))
    return redirect(reverse('admin_custom:manage_domains'))

@user_passes_test(is_admin)
def delete_activity(request, id):
    activity = get_object_or_404(Activite, pk=id)
    activity.delete()
    return redirect('admin_custom:manage_activities')


@user_passes_test(is_admin)
def manage_travel_programs(request):
    travel_programs = CarnetVoyage.objects.all()
    return render(request, 'admin/travel_programs.html', {'travel_programs': travel_programs})

@user_passes_test(is_admin)
def edit_travel_program(request, id):
    travel_program = get_object_or_404(CarnetVoyage, pk=id)
    if request.method == 'POST':
        # Update travel program fields based on form data
        travel_program.date_debut_sejour = request.POST.get('date_debut_sejour')
        travel_program.date_fin_sejour = request.POST.get('date_fin_sejour')
        travel_program.cout_total = request.POST.get('cout_total')
        travel_program.valide = 'valide' in request.POST
        travel_program.save()
        return redirect('admin_custom:manage_travel_programs')
    return render(request, 'admin/travel_programs.html', {'travel_program': travel_program})