const slides = document.querySelectorAll('.main-slide');
const previews = document.querySelectorAll('.preview');

document.addEventListener('DOMContentLoaded', () => {
    currentSlide(0);
});

function currentSlide(index) {

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

const btn = document.querySelector('.btn-submit');

btn.addEventListener('click', async function (e) {
    e.preventDefault();

    if (btn.disabled) return;

    const name = document.querySelector('.description h1').textContent;
    const user = document.querySelector('input[name="name"]').value;
    const phone = document.querySelector('input[name="phone"]').value;
    const count = document.querySelector('.count').textContent;
    const price = document.querySelector('.price').textContent;

    if (!user || !phone) return;

    btn.disabled = true;
    btn.style.background = "#ccc";
    btn.style.color = "#666";
    btn.style.cursor = "not-allowed";

    const data = {
        name: name,
        user: user,
        phone: phone,
        count: Number(count),
        price: Number(price)
    };

    try {
        const response = await fetch("/save-order", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        const msg = document.createElement('p');
        msg.style.marginTop = "10px";

        if (result.success) {

            const overlay = document.createElement('div');
            overlay.style.position = 'fixed';
            overlay.style.top = '0';
            overlay.style.left = '0';
            overlay.style.width = '100%';
            overlay.style.height = '100%';
            overlay.style.background = 'rgba(0,0,0,0.6)';
            overlay.style.backdropFilter = 'blur(5px)';
            overlay.style.zIndex = '999';

            const modal = document.createElement('div');
            modal.style.position = 'fixed';
            modal.style.top = '50%';
            modal.style.left = '50%';
            modal.style.transform = 'translate(-50%, -50%)';
            modal.style.background = '#fff';
            modal.style.padding = '30px 40px';
            modal.style.borderRadius = '15px';
            modal.style.zIndex = '1000';
            modal.style.textAlign = 'center';
            modal.style.fontSize = '18px';
            modal.style.color = 'green';
            modal.style.boxShadow = '0 10px 30px rgba(0,0,0,0.3)';
            modal.style.opacity = '0';
            modal.style.transition = '0.3s';

            modal.textContent =
                'Zamówienie zostało złożone! Skontaktujemy się z Państwem w ciągu 10 minut';

            document.body.appendChild(overlay);
            document.body.appendChild(modal);

            setTimeout(() => modal.style.opacity = '1', 10);

            let timeout = setTimeout(() => {
                overlay.remove();
                modal.remove();
                window.location.href = "/";
            }, 20000);

            // якщо клікнули — теж закриваємо, але без конфлікту з таймером
            overlay.addEventListener('click', () => {
                clearTimeout(timeout); // 🔥 важливо
                overlay.remove();
                modal.remove();
                window.location.href = "/";
            });
        } else {
            msg.textContent = 'Błąd zamówienia!';
            msg.style.color = 'red';
            btn.disabled = false;
        }

        btn.insertAdjacentElement('afterend', msg);

    } catch (error) {
        console.error(error);

        const msg = document.createElement('p');
        msg.textContent = 'Błąd połączenia!';
        msg.style.color = 'red';

        btn.insertAdjacentElement('afterend', msg);

        btn.disabled = false;
    }
});