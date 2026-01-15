from django.urls import path
from . import views

# Namespace pour éviter les conflits d'URLs
app_name = 'musique'

# Configuration de l'acheminement des requêtes (URL routing)
# Chaque URL est mappée à une vue spécifique
urlpatterns = [
    # Liste de toutes les musiques
    path('', views.liste_musiques, name='liste'),
    
    # Détails d'une musique spécifique (paramètre dynamique: id)
    path('<int:id>/', views.detail_musique, name='detail'),
    
    # Créer une nouvelle musique
    path('creer/', views.creer_musique, name='creer'),
    
    # Modifier une musique existante (paramètre dynamique: id)
    path('<int:id>/modifier/', views.modifier_musique, name='modifier'),
    
    # Supprimer une musique (paramètre dynamique: id)
    path('<int:id>/supprimer/', views.supprimer_musique, name='supprimer'),

    # API AJAX
    path('api/musiques/', views.api_musiques, name='api_musiques'),
]
