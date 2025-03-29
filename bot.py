import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text

TOKEN = os.getenv("BOT_TOKEN")  # Токен бота, укажите в переменных окружения

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Главное меню
main_menu = InlineKeyboardMarkup(row_width=1)
btn_section1 = InlineKeyboardButton("Раздел 1", callback_data="section1")
btn_section2 = InlineKeyboardButton("Раздел 2", callback_data="section2")
main_menu.add(btn_section1, btn_section2)

# Подменю разделов
def get_submenu(section):
    submenu = InlineKeyboardMarkup(row_width=1)
    submenu.add(
        InlineKeyboardButton("Подпункт 1", callback_data=f"{section}_sub1"),
        InlineKeyboardButton("Подпункт 2", callback_data=f"{section}_sub2"),
        InlineKeyboardButton("Подпункт 3", callback_data=f"{section}_sub3"),
        InlineKeyboardButton("🔙 Назад", callback_data="back")
    )
    return submenu

# Данные для подпунктов
subsections = {
    "section1_sub1": ("https://via.placeholder.com/400", "Описание для Раздела 1 - Подпункт 1"),
    "section1_sub2": ("https://via.placeholder.com/400", "Описание для Раздела 1 - Подпункт 2"),
    "section1_sub3": ("https://via.placeholder.com/400", "Описание для Раздела 1 - Подпункт 3"),
    "section2_sub1": ("https://via.placeholder.com/400", "Описание для Раздела 2 - Подпункт 1"),
    "section2_sub2": ("https://via.placeholder.com/400", "Описание для Раздела 2 - Подпункт 2"),
    "section2_sub3": ("https://via.placeholder.com/400", "Описание для Раздела 2 - Подпункт 3"),
}

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Выберите раздел:", reply_markup=main_menu)

# Обработчик нажатия на разделы
@dp.callback_query_handler(lambda c: c.data in ["section1", "section2"])
async def open_section(callback_query: types.CallbackQuery):
    section = callback_query.data
    await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                message_id=callback_query.message.message_id,
                                text="Выберите подпункт:",
                                reply_markup=get_submenu(section))

# Обработчик нажатия на подпункты
@dp.callback_query_handler(lambda c: c.data in subsections)
async def send_subsection(callback_query: types.CallbackQuery):
    img_url, text = subsections[callback_query.data]
    submenu = get_submenu(callback_query.data.split("_")[0])
    
    await bot.send_photo(chat_id=callback_query.message.chat.id, photo=img_url, caption=text, reply_markup=submenu)
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)

# Обработчик кнопки "Назад"
@dp.callback_query_handler(Text(equals="back"))
async def go_back(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                message_id=callback_query.message.message_id,
                                text="Выберите раздел:",
                                reply_markup=main_menu)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
