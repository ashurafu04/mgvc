from django.db import models
from comptes.models import Administrateur


class Domaine(models.Model):
    """
    Domaine d'activité (ex: sport, restauration, bien-être...)
    """
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    gestionnaire = models.ForeignKey(
        Administrateur, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='domaines_geres'
    )
    
    class Meta:
        verbose_name = "Domaine d'activité"
        verbose_name_plural = "Domaines d'activités"
    
    def __str__(self):
        return self.nom
    
    def lister_activites(self):
        """Renvoie toutes les activités de ce domaine"""
        return self.activites.filter(disponible=True)


class Activite(models.Model):
    """
    Activité proposée par le club de vacances
    """
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    cout = models.DecimalField(max_digits=10, decimal_places=2)
    disponible = models.BooleanField(default=True)
    capacite_max = models.PositiveIntegerField(default=0)  # 0 = illimité
    duree = models.PositiveIntegerField(default=0, help_text="Duration in minutes")
    date_creation = models.DateTimeField(auto_now_add=True)
    domaine = models.ForeignKey(
        Domaine, 
        on_delete=models.CASCADE,
        related_name='activites'
    )
    gestionnaire = models.ForeignKey(
        Administrateur, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='activites_gerees'
    )
    photo = models.ImageField(upload_to='activite_photos/', blank=True, null=True)
    
    class Meta:
        verbose_name = "Activité"
        verbose_name_plural = "Activités"
    
    def __str__(self):
        return f"{self.nom} ({self.domaine.nom})"