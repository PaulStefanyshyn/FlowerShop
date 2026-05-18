def format_order(order: dict) -> str:
    return (
        "🌸 Нове замовлення\n\n"
        f"💐 Букет: {order['bouquet_name']}\n"
        f"👤 Ім'я: {order['lead_name']}\n"
        f"📞 Телефон: {order['lead_phone']}\n"
        f"📅 Дата: {order['created_at']}"
    )