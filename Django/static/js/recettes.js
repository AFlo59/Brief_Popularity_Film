$(document).ready(function() {
    $('#film_select').change(function() {
        var selectedFilmId = $(this).val();
        var selectedFilmTitle = $(this).find('option:selected').text();
        var selectedSalle = $(this).closest('div').find('h4').text();
        var pred_rct_daily = $(this).closest('div').find('.pred_rct_daily').text();
        var pred_bnf_hebdo = $(this).closest('tr').find('.pred_bnf_hebdo').text();
    
        console.log("Film sélectionné :", selectedFilmTitle);
        console.log("ID du film sélectionné :", selectedFilmId);
        console.log("Salle :", selectedSalle);
        console.log("Prédiction recette quotidienne :", pred_rct_daily);
        console.log("Prédiction bénéfice hebdomadaire :", pred_bnf_hebdo);
    });
});