from django.db import models

# Ce modèle est un exemple qui pourrait être utilisé pour des paramètres globaux
# de l'application ou des éléments partagés
class SiteConfiguration(models.Model):
    """
    Configuration globale du site
    """
    nom_site = models.CharField(max_length=100, default="Mon Carnet de Voyage")
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='core/', blank=True, null=True)
    email_contact = models.EmailField(blank=True)
    telephone_contact = models.CharField(max_length=20, blank=True)
    adresse = models.TextField(blank=True)
    
    # Réseaux sociaux
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    
    # Paramètres de l'application
    max_activites_par_jour = models.PositiveIntegerField(default=5)
    max_jours_carnet = models.PositiveIntegerField(default=30)
    
    class Meta:
        verbose_name = "Configuration du site"
        verbose_name_plural = "Configurations du site"
    
    def __str__(self):
        return self.nom_site
    
    @classmethod
    def get_config(cls):
        """
        Récupère la configuration ou crée une configuration par défaut
        """
        config, created = cls.objects.get_or_create(pk=1)
        return config