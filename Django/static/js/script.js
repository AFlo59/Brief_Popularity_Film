const toggleHeaderButton = document.getElementById('toggleHeaderButton');
const headerConteneur = document.querySelector('.header_conteneur');

toggleHeaderButton.addEventListener('click', function() {
    headerConteneur.classList.toggle('show');

    const icon = toggleHeaderButton.querySelector('i');
    if (headerConteneur.classList.contains('show')) {
        icon.classList.remove('fa-chevron-right');
        icon.classList.add('fa-chevron-left');
        headerConteneur.style.transition = 'left 0.3s ease';
        headerConteneur.style.left = '0';
    } else {
        icon.classList.remove('fa-chevron-left');
        icon.classList.add('fa-chevron-right');
        headerConteneur.style.transition = 'all 0.5s ease-out';
        headerConteneur.style.left = '-100vw';
    }
});