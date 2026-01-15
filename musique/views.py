from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib import messages
from .models import Musique
from .forms import MusiqueForm

def liste_musiques(request):
    """
    Vue pour afficher la liste de toutes les musiques (READ)
    Démontre l'utilisation de l'ORM pour récupérer toutes les entrées
    """
    musiques = Musique.objects.all().order_by('titre')
    contexte = {
        'musiques': musiques,
        'titre_page': 'Liste des musiques'
    }
    return render(request, 'musique/liste.html', contexte)

def detail_musique(request, id):
    """
    Vue pour afficher les détails d'une musique spécifique (READ)
    Démontre l'utilisation de l'ORM pour récupérer une entrée par ID
    """
    musique = get_object_or_404(Musique, pk=id)
    contexte = {
        'musique': musique,
        'titre_page': f'Détails - {musique.titre}'
    }
    return render(request, 'musique/detail.html', contexte)

def creer_musique(request):
    """
    Vue pour créer une nouvelle musique (CREATE)
    Démontre la validation côté serveur et l'utilisation de formulaires Django
    """
    if request.method == 'POST':
        formulaire = MusiqueForm(request.POST)
        if formulaire.is_valid():
            # Validation réussie, sauvegarde dans la base de données via l'ORM
            musique = formulaire.save()
            messages.success(request, f'La musique "{musique.titre}" a été ajoutée avec succès.')
            return redirect('musique:detail', id=musique.id)
        else:
            # Validation échouée, affichage des erreurs
            messages.error(request, 'Veuillez corriger les erreurs dans le formulaire.')
    else:
        formulaire = MusiqueForm()
    
    contexte = {
        'formulaire': formulaire,
        'titre_page': 'Ajouter une musique',
        'action': 'Créer'
    }
    return render(request, 'musique/formulaire.html', contexte)

def modifier_musique(request, id):
    """
    Vue pour modifier une musique existante (UPDATE)
    Démontre la mise à jour via l'ORM et la validation côté serveur
    """
    musique = get_object_or_404(Musique, pk=id)
    
    if request.method == 'POST':
        formulaire = MusiqueForm(request.POST, instance=musique)
        if formulaire.is_valid():
            # Validation réussie, mise à jour dans la base de données
            musique = formulaire.save()
            messages.success(request, f'La musique "{musique.titre}" a été modifiée avec succès.')
            return redirect('musique:detail', id=musique.id)
        else:
            messages.error(request, 'Veuillez corriger les erreurs dans le formulaire.')
    else:
        formulaire = MusiqueForm(instance=musique)
    
    contexte = {
        'formulaire': formulaire,
        'musique': musique,
        'titre_page': f'Modifier - {musique.titre}',
        'action': 'Modifier'
    }
    return render(request, 'musique/formulaire.html', contexte)

def supprimer_musique(request, id):
    """
    Vue pour supprimer une musique (DELETE)
    Démontre la suppression via l'ORM avec confirmation
    """
    musique = get_object_or_404(Musique, pk=id)
    
    if request.method == 'POST':
        titre = musique.titre
        musique.delete()  # Suppression via l'ORM
        messages.success(request, f'La musique "{titre}" a été supprimée avec succès.')
        return redirect('musique:liste')
    

    contexte = {
        'musique': musique,
        'titre_page': f'Supprimer - {musique.titre}'
    }
    return render(request, 'musique/supprimer.html', contexte)

def api_musiques(request):
    """
    API pour récupérer les musiques au format JSON via AJAX.
    Critère: Les données échangées sont structurées avec JSON.
    Critère: Au moins un appel Ajax dialogue avec la base de données.
    """
    from django.http import JsonResponse
    
    query = request.GET.get('q', '')
    
    if query:
        # Filtrage simple par titre ou artiste (insensible à la casse)
        musiques = Musique.objects.filter(Q(titre__icontains=query) | Q(artiste__icontains=query))
    else:
        musiques = Musique.objects.all()
        
    data = list(musiques.values('id', 'titre', 'artiste', 'style'))
    
    return JsonResponse({'musiques': data})
