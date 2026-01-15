from django.contrib import admin
from .models import Musique

# Enregistrement du modèle Musique dans l'interface d'administration
@admin.register(Musique)
class MusiqueAdmin(admin.ModelAdmin):
    list_display = ('titre', 'artiste', 'style')
    list_filter = ('style',)
    search_fields = ('titre', 'artiste', 'style')
    ordering = ('titre',)
