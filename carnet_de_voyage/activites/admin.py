from django.contrib import admin

# Register your models here.
from .models import Domaine, Activite

@admin.register(Domaine)
class DomaineAdmin(admin.ModelAdmin):
    list_display = ("nom", "description", "is_active", "gestionnaire")

@admin.register(Activite)
class ActiviteAdmin(admin.ModelAdmin):
    list_display = ("nom", "domaine", "disponible", "capacite_max")
    list_filter = ("domaine", "disponible")
    search_fields = ("nom", "description")
    # This will show the photo upload field in the admin form
    fields = ("nom", "description", "cout", "disponible", "capacite_max", "duree", "domaine", "gestionnaire", "photo")
