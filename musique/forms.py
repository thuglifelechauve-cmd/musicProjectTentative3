from django import forms
from .models import Musique

class MusiqueForm(forms.ModelForm):
    """Formulaire pour créer et modifier une musique avec validation côté serveur"""
    
    class Meta:
        model = Musique
        fields = ['artiste', 'titre', 'style']
        labels = {
            'artiste': 'Artiste',
            'titre': 'Titre',
            'style': 'Style musical',
        }
    

    
    def clean_artiste(self):
        """Validation: l'artiste ne peut pas être vide"""
        artiste = self.cleaned_data.get('artiste')
        if not artiste or not artiste.strip():
            raise forms.ValidationError("Le nom de l'artiste est obligatoire.")
        return artiste.strip()
    
    def clean_titre(self):
        """Validation: le titre ne peut pas être vide"""
        titre = self.cleaned_data.get('titre')
        if not titre or not titre.strip():
            raise forms.ValidationError("Le titre est obligatoire.")
        return titre.strip()
