from django.db import models
from django.contrib.auth.models import AbstractUser


class Utilisateur(AbstractUser):
    """
    Modèle utilisateur de base, extension de AbstractUser de Django
    """
    # Les champs suivants sont déjà présents dans AbstractUser:
    # username, password, email, first_name, last_name, is_active, is_staff, date_joined
    
    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"


class Client(Utilisateur):
    """
    Modèle représentant un client du club de vacances
    """
    date_naissance = models.DateField(null=True, blank=True)
    telephone = models.CharField(max_length=20, blank=True)
    
    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def creer_programme(self):
        """Créer un nouveau carnet de voyage pour le client"""
        from carnets.models import CarnetVoyage
        return CarnetVoyage.objects.create(client=self)
    
    def consulter_programmes(self):
        """Renvoie tous les carnets de voyage du client"""
        return self.carnetvoyage_set.all()


class Administrateur(Utilisateur):
    """
    Modèle représentant un administrateur du MGVC
    """
    fonction = models.CharField(max_length=100, blank=True)
    
    class Meta:
        verbose_name = "Administrateur"
        verbose_name_plural = "Administrateurs"
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.fonction})"