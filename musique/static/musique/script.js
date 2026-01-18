// Attendre que le DOM soit chargé (pas document.ready, mais l'événement standard)
document.addEventListener('DOMContentLoaded', function () {
    console.log("DOM entièrement chargé et analysé.");

    // Critère: Fonction assignée à une variable
    const searchInput = document.getElementById('searchInput');
    const resultsContainer = document.getElementById('searchResults');
    const musiquesTableBody = document.querySelector('tbody');

    // Critère: Fonction de rappel (callback) pour l'événement
    if (searchInput) {
        searchInput.addEventListener('keyup', function (event) {
            const query = event.target.value;
            console.log("Recherche pour : " + query);

            // Appel AJAX
            ajaxGet(`/musiques/api/musiques/?q=${query}`, function (response) {
                // Callback de retour de l'AJAX
                updateDOM(response);
            });
        });
    }
});

// Critère: Fonction passée en paramètre (callback)
// Critère: AJAX avec XMLHttpRequest (ancienne méthode standard demandée)
function ajaxGet(url, callback) {
    console.log(`[CLIENT] Envoi de la requête vers ${url}`);

    // Création de l'objet XMLHttpRequest
    const xhr = new XMLHttpRequest();

    // Configuration de la requête méthode GET, URL, asynchrone (true)
    xhr.open("GET", url, true);

    // Gestion de l'événement de changement d'état
    xhr.onreadystatechange = function () {
        // readyState 4 = DONE (opération terminée)
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                console.log("[CLIENT] Réponse reçue du serveur.");
                // Parsing manuel du JSON (nécessaire avec XHR contrairement au .json() de fetch)
                try {
                    const data = JSON.parse(xhr.responseText);
                    // Exécution du callback avec les données
                    callback(data);
                } catch (e) {
                    console.error("Erreur de parsing JSON:", e);
                }
            } else {
                console.error("Erreur AJAX:", xhr.status);
            }
        }
    };

    // Envoi de la requête
    xhr.send();

    console.log("[CLIENT] Requête asynchrone lancée (ce message s'affiche avant la réponse).");
}

// Critère: Modification du DOM (ajout de nœuds)
// Critère: Les relations entre noeuds
function updateDOM(data) {
    const musiques = data.musiques;
    const tbody = document.querySelector('tbody');

    // Vider le tableau actuel
    tbody.innerHTML = '';

    if (musiques.length === 0) {
        const tr = document.createElement('tr');
        const td = document.createElement('td');
        td.colSpan = 4;
        td.textContent = "Aucune musique trouvée.";
        tr.appendChild(td);
        tbody.appendChild(tr);
        return;
    }

    // Critère: Boucle (forEach)
    musiques.forEach(function (musique) {
        // Création des éléments (NOEUDS)
        const tr = document.createElement('tr'); // Parent

        const tdTitre = document.createElement('td'); // Enfant
        tdTitre.textContent = musique.titre;

        const tdArtiste = document.createElement('td'); // Enfant
        tdArtiste.textContent = musique.artiste;

        const tdStyle = document.createElement('td'); // Enfant
        tdStyle.textContent = musique.style;

        const tdActions = document.createElement('td'); // Enfant

        // Liens d'action
        const linkModif = document.createElement('a');
        linkModif.href = `/musique/${musique.id}/modifier/`;
        linkModif.textContent = "Modifier";
        linkModif.style.marginRight = "10px";

        const linkSuppr = document.createElement('a');
        linkSuppr.href = `/musique/${musique.id}/supprimer/`;
        linkSuppr.textContent = "Supprimer";

        // Assemblage de l'arbre DOM
        tdActions.appendChild(linkModif);
        tdActions.appendChild(linkSuppr);

        tr.appendChild(tdTitre);  // Relation: tr est parent de tdTitre
        tr.appendChild(tdArtiste);
        tr.appendChild(tdStyle);
        tr.appendChild(tdActions);

        // Ajout au DOM principal
        tbody.appendChild(tr);
    });

    console.log("DOM mis à jour avec " + musiques.length + " éléments.");
}
