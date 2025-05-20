from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Client
def register_view(request):
    return render(request, 'register.html')

def login_view(request):
    return render(request, 'login.html')

def register(request):
    print("Méthode :", request.method)
    print("URL appelée :", request.path)
    if request.method == 'POST':
        print("POST reçu")  
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
        return redirect('login')  # Assure-toi que l'URL 'login' existe
    else:
        print("GET reçu")  # debug
    return render(request, 'comptes/register.html')
