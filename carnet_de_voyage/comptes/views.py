from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Client
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout

def register_view(request):
    return render(request, 'register.html')

def login_view(request):
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':  
        username = request.POST.get('username')

        if Client.objects.filter(username=username).exists():
            messages.error(request, "Ce username est déjà pris.")
            return redirect('register')

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
        messages.success(request, "Inscription réussie ! Connectez-vous.")
        return redirect('login')  # nom de la vue login_view
    return render(request, 'comptes/register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, "Connexion réussie !")
            return redirect('list_programs') 
        else:
            messages.error(request, "Username ou mot de passe invalides.")
            return redirect('login') 
    return render(request, 'comptes/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')