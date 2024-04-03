function toggleDropdown() {
    var dropdown = document.getElementById("dropdown-content");
    if (dropdown.style.display === "none") {
        dropdown.style.display = "block";
    } else {
        dropdown.style.display = "none";
    }
}

// Obtenez les boutons de dropdown et ajoutez des écouteurs d'événements pour basculer les dropdowns lorsqu'ils sont cliqués
var businessGuideBtn = document.getElementById("business-guide-btn");
businessGuideBtn.addEventListener("click", function() {
    toggleDropdown("business-guide-dropdown");
});

var userBtn = document.getElementById("user-btn");
userBtn.addEventListener("click", function() {
    toggleDropdown("user-dropdown");
});

// Vérifiez si l'utilisateur est connecté
var isAuthenticated = "{{ user.is_authenticated }}";

// Si l'utilisateur est connecté, changez les boutons de connexion et d'inscription par le bouton de l'utilisateur connecté
if (isAuthenticated === "True") {
    var loginBtn = document.getElementById("login-btn");
    loginBtn.style.display = "none";
    var signupBtn = document.getElementById("signup-btn");
    signupBtn.style.display = "none";

    var username = "{{ user.get_username }}";
    userBtn.textContent = username;
}

/* When the user clicks on the button, 
toggle between hiding and showing the dropdown content */
function myFunction() {
    document.getElementById("myDropdown").classList.toggle("show");
  }
  
  // Close the dropdown if the user clicks outside of it
  window.onclick = function(event) {
    if (!event.target.matches('.dropbtn')) {
      var dropdowns = document.getElementsByClassName("dropdown-content");
      var i;
      for (i = 0; i < dropdowns.length; i++) {
        var openDropdown = dropdowns[i];
        if (openDropdown.classList.contains('show')) {
          openDropdown.classList.remove('show');
        }
      }
    }
  }