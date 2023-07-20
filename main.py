#код самого бота
#в файле secret_information хранятся переменная TOKEN с токеном бота
#и словарь MY_DICT c ключами /vk, /tg и /mail c соответствующими значениями(
#строками с ссылками)
from aiogram import Bot, Dispatcher, executor, types
import secret_information as s_i


HELP_COMMAND = """
/start - начать работу с ботом
/help - список комманд
/vk - ссылка на вк
/tg - ссылка на тг
/mail - адрес почты"""

bot = Bot(s_i.TOKEN)
dp = Dispatcher(bot)


async def on_startup(_):
    print('Бот запущен!')

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer(text='<em>Добро пожаловать!</em>', parse_mode="HTML")#ответ на сообщение
    await message.delete()


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.reply(text=HELP_COMMAND)#ответ на сообщение


@dp.message_handler(commands=['vk', 'tg', 'mail'])
async def answer(message: types.Message):
    await message.answer(text=s_i.MY_DICT[message.text])


#пасхалка ради пасхалки
@dp.message_handler(commands=['kotik'])
async def cat_command(message: types.Message):
    await bot.send_sticker(message.from_user.id, sticker="CAACAgIAAxkBAAEJwPtkua-2Nhbe04tWcOaOSPQgv_nrsAACJhkAApqrsEvfn8VCsjY8WC8E")

if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup)#типо запуск бота


