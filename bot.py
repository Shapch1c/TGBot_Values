import telebot
from config import TOKEN, CURRENCIES
from extensions import APIException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    text = (
        "Привет! Чтобы узнать цену валюты, отправь сообщение в формате:\n"
        "<валюта, которую переводим> <валюта, в которую переводим> <количество>\n"
        "Пример: доллар рубль 100\n"
        "Список доступных валют: /values"
    )
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def send_values(message):
    text = "Доступные валюты:\n" + "\n".join(CURRENCIES.keys())
    bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=['text'])
def convert(message):
    try:
        parts = message.text.split()
        if len(parts) != 3:
            raise APIException("Неверное количество параметров. Формат: <валюта1> <валюта2> <количество>")

        base, quote, amount = parts
        total = CurrencyConverter.get_price(base, quote, amount)
        text = f"{amount} {base} = {total} {quote}"
        bot.send_message(message.chat.id, text)

    except APIException as e:
        bot.send_message(message.chat.id, f"Ошибка пользователя: {e}")
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка системы: {e}")

bot.polling()