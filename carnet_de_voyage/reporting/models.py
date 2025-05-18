from django.db import models
import os
import io
import matplotlib.pyplot as plt
from collections import defaultdict
from django.conf import settings
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


class Rapport(models.Model):
    """
    Rapport généré à partir d'un carnet de voyage
    """
    FORMATS = [
        ('pdf', 'PDF'),
        ('camembert', 'Diagramme en camembert'),
    ]
    
    carnet_voyage = models.ForeignKey(
        'carnets.CarnetVoyage', 
        on_delete=models.CASCADE,
        related_name='rapports'
    )
    titre = models.CharField(max_length=200)
    date_generation = models.DateTimeField(auto_now_add=True)
    format = models.CharField(max_length=20, choices=FORMATS, default='pdf')
    fichier_url = models.FileField(upload_to='rapports/', null=True, blank=True)
    
    class Meta:
        verbose_name = "Rapport"
        verbose_name_plural = "Rapports"
    
    def __str__(self):
        return f"{self.titre} ({self.format})"
    
    def generer_pdf(self):
        """Génère un rapport PDF pour le carnet de voyage avec ReportLab"""
        # Créer le répertoire de destination s'il n'existe pas
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'rapports')
        os.makedirs(upload_dir, exist_ok=True)
        
        # Chemin du fichier PDF
        filename = f"carnet_{self.carnet_voyage.id}_{self.date_generation.strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = os.path.join(upload_dir, filename)
        
        # Utiliser ReportLab pour générer le PDF
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()
        
        # Titre
        elements.append(Paragraph(self.titre, styles['Title']))
        elements.append(Spacer(1, 12))
        
        # Informations client
        client = self.carnet_voyage.client
        elements.append(Paragraph(f"Client: {client.first_name} {client.last_name}", styles['Heading2']))
        elements.append(Paragraph(f"Dates de séjour: Du {self.carnet_voyage.date_debut_sejour} au {self.carnet_voyage.date_fin_sejour}", styles['Normal']))
        elements.append(Spacer(1, 12))
        
        # Liste des activités planifiées
        elements.append(Paragraph("Activités planifiées", styles['Heading2']))
        elements.append(Spacer(1, 6))
        
        # Créer la table des activités
        data = [['Date', 'Activité', 'Domaine', 'Horaires', 'Coût']]
        
        activites_planifiees = self.carnet_voyage.activites_planifiees.all().order_by('date_activite', 'heure_debut')
        for ap in activites_planifiees:
            data.append([
                ap.date_activite.strftime('%d/%m/%Y'),
                ap.activite.nom,
                ap.activite.domaine.nom,
                f"{ap.heure_debut.strftime('%H:%M')} - {ap.heure_fin.strftime('%H:%M')}",
                f"{ap.activite.cout} €"
            ])
        
        # Ajouter la table au PDF
        t = Table(data)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(t)
        
        # Coût total
        elements.append(Spacer(1, 12))
        elements.append(Paragraph(f"Coût total: {self.carnet_voyage.cout_total} €", styles['Heading3']))
        
        # Notes de mémoire si présentes
        notes_activities = activites_planifiees.exclude(note_memoire='')
        if notes_activities.exists():
            elements.append(Spacer(1, 12))
            elements.append(Paragraph("Notes de voyage", styles['Heading2']))
            elements.append(Spacer(1, 6))
            
            for ap in notes_activities:
                elements.append(Paragraph(f"{ap.date_activite.strftime('%d/%m/%Y')} - {ap.activite.nom}:", styles['Heading4']))
                elements.append(Paragraph(ap.note_memoire, styles['Normal']))
                elements.append(Spacer(1, 6))
        
        # Générer le PDF
        doc.build(elements)
        
        # Enregistrer l'URL du fichier
        relative_path = os.path.join('rapports', filename)
        self.fichier_url = relative_path
        self.save()
        
        return self.fichier_url
    
    def generer_camembert(self):
        """Génère un diagramme camembert des activités par domaine"""
        # Regrouper les activités par domaine
        domaines_data = defaultdict(float)
        
        for ap in self.carnet_voyage.activites_planifiees.all():
            domaine_nom = ap.activite.domaine.nom
            domaines_data[domaine_nom] += float(ap.activite.cout)
        
        # Créer le camembert avec matplotlib
        plt.figure(figsize=(10, 8))
        plt.pie(
            domaines_data.values(), 
            labels=domaines_data.keys(), 
            autopct='%1.1f%%', 
            startangle=90,
            shadow=True
        )
        plt.axis('equal')  # Cercle parfait
        plt.title(f"Répartition des activités par domaine\n{self.carnet_voyage.client}", pad=20)
        
        # Sauvegarder l'image
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'rapports')
        os.makedirs(upload_dir, exist_ok=True)
        
        filename = f"camembert_{self.carnet_voyage.id}_{self.date_generation.strftime('%Y%m%d_%H%M%S')}.png"
        filepath = os.path.join(upload_dir, filename)
        
        plt.savefig(filepath, bbox_inches='tight')
        plt.close()
        
        # Enregistrer l'URL du fichier
        relative_path = os.path.join('rapports', filename)
        self.fichier_url = relative_path
        self.save()
        
        return self.fichier_url