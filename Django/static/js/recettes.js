$(document).ready(function () {
    // Fonction pour mettre à jour les données des films sélectionnés
    function updateFilmData(filmData) {
        // Boucle sur les données des films
        $.each(filmData, function (index, film) {
            updateOneFilm(film, index + 1)
        });
    }

    function updateOneFilm(film, index = 0) {
        // Mise à jour des éléments HTML avec les données des films
        $('#pred_rct_daily_' + index).text(film.pred_rct_daily);
        $('#pred_bnf_hebdo_' + index).text(film.pred_bnf_hebdo);

        // Ajout d'un console.log() pour vérifier les données
        console.log("Film " + index + " : Rct = " + film.pred_rct_daily + ", Bnf = " + film.pred_bnf_hebdo);
    }

    // Écouteur d'événements pour le changement de sélection de film
    $('.film-select').change(function () {
        var filmId = $(this).val(); // Récupérer l'ID du film sélectionné
        var index = $(this).attr('data-index') * 1

        // Requête AJAX pour obtenir les données du film sélectionné
        $.ajax({
            url: '/funct/get_data/', // Utilisation de l'URL correcte
            method: 'GET',
            data: { film: filmId, salle: index },
            success: function (response) {
                updateOneFilm(response.film, index);
            },
            error: function (xhr, status, error) {
                console.error('Erreur lors de la récupération des données du film:', error);
            }
        });
    });
});