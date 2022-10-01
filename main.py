import telebot
from conf import TOKEN, keys
from extensions import Converter, APIException


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def test(message: telebot.types.Message):
    text = 'Чтобы начать работу, введите команду в формате:\n <валюта> <в какую валюту перевести> <сумма>\n' \
'Список всех доступных валют /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def test(message: telebot.types.Message):
    text = 'Доступные валюты:'

    for key in keys.keys():
        text = '\n'.join((text, key, ))

    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def test(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Неверное количество параметров, должно быть 3')

        quote, base, amount = values
        total_base = Converter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')

    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()
