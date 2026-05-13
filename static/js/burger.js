const burger = document.querySelector('.burger');
const navbar = document.querySelector('.navbar');
const overlay = document.querySelector('.overlay');
const links = document.querySelectorAll('.navbar a');

function closeMenu() {
    burger.classList.remove('active');
    navbar.classList.remove('active');
    overlay.classList.remove('active');
    document.body.classList.remove('no-scroll');
}

burger.addEventListener('click', () => {
    burger.classList.toggle('active');
    navbar.classList.toggle('active');
    overlay.classList.toggle('active');
    document.body.classList.toggle('no-scroll');
});

navbar.addEventListener('click', closeMenu);

links.forEach(link => {
    link.addEventListener('click', closeMenu);
});