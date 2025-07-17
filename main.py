import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, F, html, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from my_time import get_time
from weather import get_weather, get_weather_info


# Bot token can be obtained via https://t.me/BotFather
TOKEN = getenv("BOT_TOKEN")

# All handlers should be attached to the Router (or Dispatcher)

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    logging.info(f"Зашел новый пользователь - {message.from_user.full_name}, {message.from_user.id}")
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")


@dp.message(Command("weather"))
async def weather_handler(message: Message) -> None:
    weather_data = get_weather()
    await message.answer(f"Температура: {weather_data['temperature']}C, "
                         f"ветер: {weather_data['wind']} км/ч.")


@dp.message(Command("buttons"))
async def buttons_handler(message: Message) -> None:
    logging.info('Показываем кнопки в сообщении')
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Кнопка 1",
        callback_data="button1",
    ))
    builder.add(types.InlineKeyboardButton(
        text="Яндекс",
        url="https://ya.ru",  # Открывает ссылку
    ))
    builder.adjust(2)  # 1 кнопка в строке (можно 2, 3...)

    await message.answer(
        "Сообщение с inline-кнопками:",
        reply_markup=builder.as_markup()
    )


@dp.callback_query(F.data == "button1")
async def handle_button1(callback: types.CallbackQuery):
    await callback.answer("Вы нажали Кнопку 1!", show_alert=True)


@dp.message(Command("services"))
async def services_handler(message: Message) -> None:
    logging.info('Показываем кнопки сервисов в сообщении')
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Погода",
        callback_data="weather",
    ))
    builder.add(types.InlineKeyboardButton(
        text="Время",
        callback_data="time",
    ))
    builder.adjust(2)  # 1 кнопка в строке (можно 2, 3...)

    await message.answer(
        "Выберите сервис:",
        reply_markup=builder.as_markup()
    )


@dp.callback_query(F.data == "weather")
async def handle_weather(callback: types.CallbackQuery):
    logging.info('выводим погоду')
    weather_data = get_weather_info()
    await callback.answer(f"Температура: {weather_data['temperature']}, "
                          f"ветер: {weather_data['wind']}.", show_alert=True)


@dp.callback_query(F.data == "time")
async def handle_time(callback: types.CallbackQuery):
    logging.info('выводим время')
    await callback.message.answer(get_time())


@dp.message()
async def echo_handler(message: Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    try:
        # Send a copy of the received message
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    logging.basicConfig(level=logging.ERROR, stream=sys.stdout)
    asyncio.run(main())
