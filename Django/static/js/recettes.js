$(document).ready(function() {
    // Fonction pour mettre à jour les données des films sélectionnés
    function updateFilmData(filmData) {
        // Boucle sur les données des films
        $.each(filmData, function(index, film) {
            // Mise à jour des éléments HTML avec les données des films
            $('#pred_rct_daily_' + (index + 1)).text(film.pred_rct_daily);
            $('#pred_bnf_hebdo_' + (index + 1)).text(film.pred_bnf_hebdo);
    
            // Ajout d'un console.log() pour vérifier les données
            console.log("Film " + (index + 1) + " : Rct = " + film.pred_rct_daily + ", Bnf = " + film.pred_bnf_hebdo);
        });
    }

    // Écouteur d'événements pour le changement de sélection de film
    $('.film-select').change(function() {
        var filmId = $(this).val(); // Récupérer l'ID du film sélectionné

        // Requête AJAX pour obtenir les données du film sélectionné
        $.ajax({
            url: '/funct/get_data/', // Utilisation de l'URL correcte
            method: 'GET',
            data: { film: filmId },
            success: function(response) {
                var filmData = response['response-data'];
                updateFilmData(filmData);
            },
            error: function(xhr, status, error) {
                console.error('Erreur lors de la récupération des données du film:', error);
            }
        });
    });
});