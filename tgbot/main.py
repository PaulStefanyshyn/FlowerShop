import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

from config import Config
from db import get_new_orders
from formatter import format_order
from state import load_state, save_state

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

bot = Bot(token=Config.BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        "Бот працює ✅\n\n"
        f"CHAT_ID цього чату:\n{message.chat.id}"
    )


@dp.message()
async def debug_chat_id_handler(message: Message):
    logging.info("CHAT_ID цього чату: %s", message.chat.id)


async def orders_worker():
    state = load_state()
    last_id = state.get("last_id", 0)

    logging.info("Worker started. Last ID: %s", last_id)

    while True:
        try:
            if Config.CHAT_ID is None:
                logging.warning("CHAT_ID не заданий у .env. Розсилка заявок пропущена.")
                await asyncio.sleep(60)
                continue

            orders = await get_new_orders(last_id)

            for order in orders:
                text = format_order(order)

                await bot.send_message(
                    chat_id=Config.CHAT_ID,
                    text=text,
                )

                last_id = order["id"]
                save_state({"last_id": last_id})

                logging.info("Order sent. ID: %s", last_id)

        except Exception as error:
            logging.exception("Worker error: %s", error)

        await asyncio.sleep(60)


async def main():
    if not Config.BOT_TOKEN or Config.BOT_TOKEN == "your_telegram_bot_token":
        raise RuntimeError("BOT_TOKEN не заданий у .env")

    asyncio.create_task(orders_worker())

    logging.info("Bot polling started")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())