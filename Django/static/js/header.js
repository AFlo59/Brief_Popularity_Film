// Fonction pour afficher ou masquer le dropdown
function toggleDropdown() {
    var dropdown = document.getElementById("dropdown-content");
    if (dropdown.style.display === "none") {
        dropdown.style.display = "block";
    } else {
        dropdown.style.display = "none";
    }
}

// Événement au chargement de la page
window.onload = function() {
    // Récupérer l'état de connexion de l'utilisateur depuis la variable 'isAuthenticated'
    var isAuthenticated = "{{ user.is_authenticated }}";

    // Sélectionner les éléments HTML du bouton de connexion et du bouton de bienvenue
    var loginBtn = document.getElementById("login-btn");
    var userBtn = document.getElementById("user-btn");

    // Si l'utilisateur est connecté
    if (isAuthenticated === "True") {
        // Masquer le bouton de connexion
        loginBtn.style.display = "none";
        // Afficher le bouton de bienvenue avec le nom de l'utilisateur
        userBtn.style.display = "block";
    } else {
        // Si l'utilisateur n'est pas connecté, afficher le bouton de connexion
        loginBtn.style.display = "block";
        // Masquer le bouton de bienvenue
        userBtn.style.display = "none";
    }
};
