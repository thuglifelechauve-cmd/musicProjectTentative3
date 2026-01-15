from django.db import models

# Modèle pour représenter une musique
class Musique(models.Model):
    artiste = models.CharField(max_length=200, verbose_name="Artiste")
    titre = models.CharField(max_length=200, verbose_name="Titre")
    style = models.CharField(max_length=100, verbose_name="Style")
    
    class Meta:
        verbose_name = "Musique"
        verbose_name_plural = "Musiques"
    
    def __str__(self):
        return f"{self.titre} - {self.artiste}"
