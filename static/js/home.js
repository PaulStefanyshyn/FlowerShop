document.querySelectorAll('.card').forEach(card => {

    const countEl = card.querySelector('.count');
    const name = card.querySelector('h1');
    const price = card.querySelector('h2');
    const order_button = card.querySelector('.order-button');

    const start_price = Number(price.textContent);

    card.addEventListener('click', (e) => {

        if (e.target.classList.contains('minus')) {
            countEl.textContent = Math.max(1, Number(countEl.textContent) - 1);
        }

        if (e.target.classList.contains('plus')) {
            countEl.textContent = Number(countEl.textContent) + 1;
        }

        price.textContent = Number(countEl.textContent) * start_price;

        order_button.addEventListener("click", async function () {
            const data = {
                name: name.textContent,
                price: Number(price.textContent),
                count: Number(countEl.textContent)
            };

            const response = await fetch("/save-data", {
                method: "POST",
                headers: {
                "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (result.success) {
                window.location.href = "/bouquets";
            }
        });

    });

});