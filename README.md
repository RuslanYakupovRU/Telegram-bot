Телеграмм бот для создания заявок

Этот телеграмм бот позволяет пользователям создавать заявки по услугам "Домофония" и "Пожарная сигнализация". 
После выбора услуги, адреса и заполнения дополнительной информации, заявка отправляется в указанный канал для дальнейшей обработки.

Основные функции:

Пользователь выбирает услугу ("Домофония" или "Пожарная сигнализация").
Пользователь выбирает адрес для заявки.
Пользователь указывает номер квартиры.
Пользователь вводит причину заявки и номер телефона.
Создается текстовое сообщение с информацией о заявке и отправляется в указанный канал.
Пользователь получает уведомление о создании заявки и может отметить ее как выполненную.
#%%
Подключение необходимых библиотек и модулей
#%%
import telebot
from telebot import types
import datetime
#%%
Установка TOKEN и CHANNEL_ID
TOKEN - это уникальный ключ бота, который выдается при его создании. CHANNEL_ID - это идентификатор канала, куда будут отправляться заявки.
#%%
TOKEN = 'СЮДА ВСТАВЛЯЕТЕ НОМЕР СВОЕГО ТОКЕНА'
CHANNEL_ID = 'СЮДА ВСТАВЛЯЕТЕ ID КАНАЛА через знак - ПРИМЕР (-1001234567890)'
bot = telebot.TeleBot(TOKEN)
user_states = {}
#%%
Обработка команды '/start'
#%%
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('Домофония'), types.KeyboardButton('Пожарная сигнализация'))
    bot.send_message(chat_id=message.chat.id, text="Выберите услугу:", reply_markup=markup)
#%%
Выбор услуги
#%%
@bot.message_handler(regexp='Домофония|Пожарная сигнализация')
def service_menu(message):
    service = message.text
    user_states[message.chat.id] = {'service': service, 'address': None, 'apartment': None, 'reason': None}
    # ...
#%%
При выборе услуги она сохраняется в словаре user_states с ключом, соответствующим чату пользователя.
#%%
Выбор адреса
#%%
# ...
    markup.add(*[types.KeyboardButton(address) for address in addresses])
    bot.send_message(chat_id=message.chat.id, text=f"Выберите адрес для заявки по {service}:", reply_markup=markup)
#%%
Пользователю предлагается выбрать адрес из списка, который зависит от выбранной ранее услуги.
#%%
Ввод номера квартиры и причины заявки
#%%
def handle_apartment(message):
    user_states[message.chat.id]['apartment'] = message.text
    # ...

def handle_reason(message):
    user_states[message.chat.id]['reason'] = message.text
    # ...
#%%
После выбора адреса пользователю предлагается ввести номер квартиры и причину заявки. 
Введенные данные сохраняются в словаре user_states.
#%%
Отправка заявки
#%%
message_text = f"Новая заявка:\n\n" \
                   f"Адрес: {selected_address}\n" \
                   f"Квартира: {apartment}\n" \
                   f"Услуга: {service}\n" \
                   f"Причина: {reason}\n" \
                   f"Дата и время: {current_time}"
    # ...
    bot.send_message(chat_id=CHANNEL_ID, text=message_text, reply_markup=markup)
#%%
После ввода всех данных создается текст заявки и отправляется в канал с указанным CHANNEL_ID.
#%%
Обработка сообщений, не удовлетворяющих предыдущим обработчикам
#%%
@bot.message_handler(content_types=['text'])
def any_msg(message):
    start(message)
#%%
Если сообщение не удовлетворяет условиям предыдущих обработчиков, то вызывается функция start(message), начинающая диалог сначала.
#%%
Запуск бота
#%%
bot.polling(none_stop=True)
#%%
Начинается бесконечный цикл получения новых обновлений от сервера Telegram.
