// Sélection du bouton
const toggleHeaderButton = document.getElementById('toggleHeaderButton');

// Sélection du header_conteneur
const headerConteneur = document.querySelector('.header_conteneur');

// Ajout d'un gestionnaire d'événement au clic sur le bouton
toggleHeaderButton.addEventListener('click', function() {
    // Toggle de la classe 'show' sur le header_conteneur
    headerConteneur.classList.toggle('show');

    // Changement de l'icône du bouton en fonction de l'état du header_conteneur
    const icon = toggleHeaderButton.querySelector('i');
    if (headerConteneur.classList.contains('show')) {
        // Si le header_conteneur est affiché, changer l'icône en chevron gauche
        icon.classList.remove('fa-chevron-right');
        icon.classList.add('fa-chevron-left');
    } else {
        // Sinon, changer l'icône en chevron droit
        icon.classList.remove('fa-chevron-left');
        icon.classList.add('fa-chevron-right');
    }
});
