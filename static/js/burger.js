const burger = document.querySelector('.burger');
const navbar = document.querySelector('.navbar');
const overlay = document.querySelector('.overlay');

burger.addEventListener('click', () => {

    burger.classList.toggle('active');

    navbar.classList.toggle('active');

    overlay.classList.toggle('active');

    document.body.classList.toggle('no-scroll');

});

overlay.addEventListener('click', () => {

    burger.classList.remove('active');

    navbar.classList.remove('active');

    overlay.classList.remove('active');

    document.body.classList.remove('no-scroll');

});