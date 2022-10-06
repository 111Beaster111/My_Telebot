import telebot
from extensions import ConvertException, CryptoConverter
from config import keys, TOKEN

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help_(message: telebot.types.Message):
    text = 'Что бы начать работу, введите боту команду в формате: \n <имя валюты>' \
    '\n<в какую валюту перевести>' \
    '\n<количество переводимой валюты>' \
    '\n<что бы увидеть список доступных валют, введите команду' \
    '\n /values>'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def currencies(message: telebot.types.Message):
    text = 'Вам доступны следующие валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):

    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertException('Неправильное количество параметров.')

        quote, base, amount = values
        total = CryptoConverter.get_price(quote, base, amount)
    except ConvertException as e:
        bot.reply_to(message, f'Ошибка пользователя \n {e}')
    except Exception as e:
        bot.reply_to(message,f'Не удалось обработать команду \n {e}')
    else:
        if float(amount) > 1:
            total = float(total) * float(amount)
            total = str(total)
            text = f'Цена {amount} {quote} в {base} составляет {total}'
            bot.send_message(message.chat.id, text)
        else:
            text = f'Цена {amount} {quote} в {base} составляет {total}'
            bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)