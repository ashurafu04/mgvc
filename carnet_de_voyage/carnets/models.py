from django.db import models
from django.utils import timezone
from comptes.models import Client
from activites.models import Activite
from django.db.models.signals import post_delete
from django.dispatch import receiver


class CarnetVoyage(models.Model):
    """
    Carnet de voyage d'un client, contenant les activités planifiées
    """
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_debut_sejour = models.DateField(null=True, blank=True)
    date_fin_sejour = models.DateField(null=True, blank=True)
    cout_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valide = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_validation = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Carnet de voyage"
        verbose_name_plural = "Carnets de voyage"
    
    def __str__(self):
        return f"Carnet de {self.client} ({self.date_debut_sejour} au {self.date_fin_sejour})"
    
    def calculer_cout_total(self):
        """Calcule le coût total des activités planifiées"""
        total = sum(act.activite.cout for act in self.activites_planifiees.all())
        self.cout_total = total
        self.save()
        return total
    
    @property
    def duree_totale(self):
        """Calcule la durée totale de toutes les activités en heures"""
        return round(sum(act.duree for act in self.activites_planifiees.all()), 1)
    
    def valider_carnet(self):
        """Valide le carnet et le soumet au Club"""
        self.valide = True
        self.date_validation = timezone.now()
        self.save()
    
    def generer_rapport(self, format="pdf"):
        """Génère un rapport pour ce carnet de voyage"""
        from reporting.models import Rapport
        rapport = Rapport.objects.create(
            carnet_voyage=self,
            titre=f"Rapport de voyage - {self.client}",
            format=format
        )
        
        if format == "pdf":
            rapport.generer_pdf()
        elif format == "camembert":
            rapport.generer_camembert()
        
        return rapport
    
    @property
    def est_modifiable(self):
        """Vérifie si le carnet peut encore être modifié"""
        return not self.valide


class ActivitePlanifiee(models.Model):
    """
    Une activité planifiée dans un carnet de voyage
    """
    carnet_voyage = models.ForeignKey(
        CarnetVoyage, 
        on_delete=models.CASCADE,
        related_name='activites_planifiees'
    )
    activite = models.ForeignKey(
        Activite, 
        on_delete=models.CASCADE,
        related_name='planifications'
    )
    date_activite = models.DateField()
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()
    note_memoire = models.TextField(blank=True)
    date_note = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Activité planifiée"
        verbose_name_plural = "Activités planifiées"
        ordering = ['date_activite', 'heure_debut']
    
    def __str__(self):
        return f"{self.activite.nom} - {self.date_activite} ({self.heure_debut}-{self.heure_fin})"
    
    def ajouter_note_memoire(self, texte):
        """Ajoute une note mémoire à l'activité planifiée"""
        self.note_memoire = texte
        self.date_note = timezone.now()
        self.save()
    
    def modifier_note_memoire(self, texte):
        """Modifie la note mémoire existante"""
        self.note_memoire = texte
        self.date_note = timezone.now()
        self.save()
        
    @property
    def duree(self):
        """Calcule la durée de l'activité en heures"""
        from datetime import datetime, timedelta
        
        debut = datetime.combine(datetime.today(), self.heure_debut)
        fin = datetime.combine(datetime.today(), self.heure_fin)
        
        # Si l'heure de fin est avant l'heure de début, on ajoute un jour
        if fin < debut:
            fin += timedelta(days=1)
            
        duree = fin - debut
        return duree.total_seconds() / 3600  # Durée en heures


@receiver(post_delete, sender=ActivitePlanifiee)
def update_cout_total_on_delete(sender, instance, **kwargs):
    """Met à jour le coût total du carnet quand une activité est supprimée"""
    instance.carnet_voyage.calculer_cout_total()