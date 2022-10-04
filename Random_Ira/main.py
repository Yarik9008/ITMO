from RovLogging import RovLogger
from random import sample
import telebot

# путь до текстового файлика с названиями географических мест
PATH = 'C:/Users/Yarik/Documents/ITMO_1/Random_Ira/name.txt'

TOKEN = '5685174221:AAFfxWguOdEoHGZl_MIwFtIGBw5S40S0enY'

log_config = {'path_log': PATH,
              'log_level': 'debug'}
logi = RovLogger(log_config)

bot = telebot.TeleBot(TOKEN)
logi.info('init telegram bot')


'''
random_10 - random geographic points
'''


def read_to_list(path: str):
    # функция парсинга файла с данными
    with open(path, encoding="utf8") as file:
        data_out = []
        for a in [i[:-1].strip() for i in file.readlines()]:
            if a != '':
                data_out.append(a)
        return data_out


data_mass = list(set(read_to_list(PATH)))
logi.info('Data : ' + str(data_mass))


def random_out(data: list, quantity: int):
    # функция выдачи заданного количество элементов их массива данных
    data = sample(data, quantity)
    str_out = ''
    for i in range(len(data)):
        name = data[i]
        i += 1
        str_out += f'{i}) {name}\n'
        i -= 1
    return str_out


@bot.message_handler(commands=['random_10'])
def random_10_out(message):
    data = random_out(data_mass, 10)
    bot.send_message(message.chat.id, data)
    logi.debug(f'User: {message.from_user.username} Data: {data}')


bot.infinity_polling()
