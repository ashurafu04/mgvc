from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Client
from django.contrib.auth import authenticate, login as auth_login

def register_view(request):
    return render(request, 'register.html')

def login_view(request):
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        date_naissance = request.POST.get('date_naissance')
        telephone = request.POST.get('telephone')

        client = Client(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            date_naissance=date_naissance,
            telephone=telephone
        )
        client.set_password(password)
        client.save()
        return redirect('login-client') 
    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password) 

        if user is not None:
            auth_login(request, user)
            messages.success(request, 'Vous êtes maintenant connecté.')
            return redirect('home')
        else:
            messages.error(request, 'Identifiants invalides. Veuillez réessayer.')
            return render(request, 'login.html')
    return redirect('login')  # Changed from 'login-view' to 'login'