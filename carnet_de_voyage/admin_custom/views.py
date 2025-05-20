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