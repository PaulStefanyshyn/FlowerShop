const slides = document.querySelectorAll('.main-slide');
const previews = document.querySelectorAll('.preview');

function currentSlide(index){

    slides.forEach(slide => {
        slide.classList.remove('active');
    });

    previews.forEach(preview => {
        preview.classList.remove('active');
    });

    slides[index].classList.add('active');
    previews[index].classList.add('active');
}

const count = document.querySelector('.count');
const price = document.querySelector('.price');
const counter = document.querySelector('.counter');
const start_price = Number(price.textContent) / Number(count.textContent);

counter.addEventListener('click', (e) => {

        if (e.target.classList.contains('minus')) {
            count.textContent = Math.max(1, Number(count.textContent) - 1);
        }

        if (e.target.classList.contains('plus')) {
            count.textContent = Number(count.textContent) + 1;
        }

        price.textContent = Number(count.textContent) * start_price;

    });