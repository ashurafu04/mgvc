from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test

def is_admin(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(is_admin)
def manage_domains(request):
    return render(request, 'admin/domains.html', {
        'domains': []  # Will be replaced with actual domains
    })

@user_passes_test(is_admin)
def add_domain(request):
    if request.method == 'POST':
        # This will be implemented later to handle domain creation
        return redirect('admin_custom:admin_domains')
    return redirect('admin_custom:admin_domains')

@user_passes_test(is_admin)
def manage_activities(request):
    return render(request, 'admin/activities.html', {
        'activities': [],  # Will be replaced with actual activities
        'domains': []  # Will be replaced with actual domains
    })

@user_passes_test(is_admin)
def add_activity(request):
    if request.method == 'POST':
        # This will be implemented later to handle activity creation
        return redirect('admin_custom:admin_activities')
    return redirect('admin_custom:admin_activities')


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
    return render(request, 'travel_program_detail.html', {'travel_program': travel_program})

def edit_activity(request, id):
    if request.method == 'POST':
        # Handle form submission
        return redirect('admin_custom:program_detail', id=id)
    activity = None  # Fetch the activity by id
    return render(request, 'edit_activity.html', {'activity': activity})

def travel_report(request):
    report_url = ""  # Generate or fetch the report URL
    return render(request, 'travel_report.html', {'report_url': report_url})