#код самого бота
#в файле secret_information хранится переменная TOKEN с токеном бота
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
import secret_information as s_i
import validators


MY_DICT = {'github': 'https://github.com/soltiste'}

bot = Bot(s_i.TOKEN)
dp = Dispatcher(bot)
kb1 = ReplyKeyboardMarkup(resize_keyboard=True)
kb1.add(KeyboardButton('/change')).insert(KeyboardButton('/links'))



async def on_startup(_):
    print('Я запустился!')


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer(text='<em>Добро пожаловать!</em> \n' 
                              'Это бот для хранения ссылок на ваши соцсети.' +
                              'Нажмите /change, чтобы узнать, как добавить новую или удалить ненужную, и /links,' +
                              'чтобы просмотреть имеющиеся.',
                         parse_mode="HTML",
                         reply_markup=kb1)#ответ на сообщение
    await message.delete()



@dp.message_handler(commands=['change'])
async def add_command(message: types.Message):
    await message.reply(text='Чтобы добавить новую ссылку, напишите ниже команду /add, пробел, далее через знак двоеточия ' +
                             '+ пробел ее название и саму ссылку одним сообщением. Например: \n/add vk: https://vk.com \n' +
                             'Чтобы удалить ссылку, напишите /delete, пробел и название ссылки в чат одним сообщением.' +
                             ' Например: \n/delete vk')#ответ на сообщение
@dp.message_handler(commands=['add'])
async def add_command(message: types.Message):
    if len(message.text) > 5:
        my_str = message.text[5:]
        if (': ' in my_str) and my_str[:2] != ': ':
            k, v = (my_str + ' ').split(': ')
            if (v != ' ') and validators.url(v[:-1]):
                MY_DICT[k] = v[:-1]
                await message.reply(text='Ссылка успешно добавлена')  # ответ на сообщение
            else:
                await message.reply(text='Что-то не так с ссылкой, попробуйте еще раз')
        else:
            await message.reply(text='Что-то не так с двоеточием и пробелом, попробуйте еще раз')
    else:
        await message.reply(text='Вы ничего не написали, попробуйте еще раз')

@dp.message_handler(commands=['delete'])
async def add_command(message: types.Message):
    if len(message.text) > 8:
        nazv = message.text[8:]
        if nazv in MY_DICT:
            del MY_DICT[nazv]
            await message.reply(text='Ссылка удалена',
                                reply_markup=kb1)
        else:
            await message.reply(text='Такой ссылки нет')
    else:
        await message.reply(text='Вы не написали название, попробуйте еще раз')


@dp.message_handler(commands=['links'])
async def links_command(message: types.Message):
    if len(list(MY_DICT.keys())) < 1:
        await message.reply(text='Вы еще не добавили ни одной ссылки!' +
                                 ' Отправьте /help, чтобы узнать, как это сделать')

    else:
        ikb = InlineKeyboardMarkup(row_width=1)
        for s in MY_DICT.keys():
            bu = InlineKeyboardButton(text=s, url=MY_DICT[s])
            ikb.add(bu)

        await bot.send_message(chat_id=message.from_user.id,
                               text='ваши ссылки:',
                               reply_markup=ikb)


@dp.message_handler(commands=list(MY_DICT.keys()))
async def answer_command(message: types.Message):
    await message.answer(text=MY_DICT[message.text[1:]])


#пасхалка ради пасхалки
@dp.message_handler(commands=['kotik'])
async def cat_command(message: types.Message):
    await bot.send_sticker(message.from_user.id, sticker="CAACAgIAAxkBAAEJwPtkua-2Nhbe04tWcOaOSPQgv_nrsAACJhkAApqrsEvfn8VCsjY8WC8E")

if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup)#типо запуск бота


