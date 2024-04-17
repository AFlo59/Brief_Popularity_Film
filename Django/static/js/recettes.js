document.addEventListener('DOMContentLoaded', function() {
    // Fonction pour charger les films disponibles dans les salles de cinéma
    function chargerFilmsDisponibles() {
        // Faire une requête AJAX pour récupérer les films disponibles depuis la vue Django
        fetch('/chemin/vers/votre/vue/django/recettes_page/')
            .then(response => response.json())
            .then(data => {
                // Construire le contenu HTML à partir des données reçues
                let contenuHTML = '';
                for (let jour in data.films_disponibles) {
                    contenuHTML += `<h2>${jour}</h2>`;
                    for (let salle in data.films_disponibles[jour]) {
                        contenuHTML += `<h3>${salle}</h3>`;
                        if (data.films_disponibles[jour][salle].length === 0) {
                            contenuHTML += `<p>Aucun film disponible pour cette salle.</p>`;
                        } else {
                            contenuHTML += `<ul>`;
                            data.films_disponibles[jour][salle].forEach(film => {
                                contenuHTML += `<li>${film.titre}</li>`; // Remplacez "titre" par le champ approprié
                            });
                            contenuHTML += `</ul>`;
                        }
                    }
                }
                // Mettre à jour le contenu de la div films_disponibles
                document.getElementById('films_disponibles').innerHTML = contenuHTML;
            })
            .catch(error => console.error('Erreur lors de la récupération des films disponibles :', error));
    }

    // Charger les films disponibles au chargement de la page
    chargerFilmsDisponibles();
});