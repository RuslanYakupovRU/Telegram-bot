

import telebot
from telebot import types
import datetime


TOKEN = 'TOKEN'
CHANNEL_ID = '-CHANNEL_ID'
bot = telebot.TeleBot(TOKEN)
user_states = {}


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('Домофония'), types.KeyboardButton('Пожарная сигнализация'))
    bot.send_message(chat_id=message.chat.id, text="Выберите услугу:", reply_markup=markup)


@bot.message_handler(regexp='Домофония|Пожарная сигнализация')
def service_menu(message):
    service = message.text
    user_states[message.chat.id] = {'service': service, 'address': None, 'apartment': None, 'reason': None}

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    if service == 'Домофония':
        addresses = ['Ул. Аметьевская магистраль д 18 к 3', 'Ул. Аметьевская магистраль д 18 к 5', 'Ул. Седова',
                     'Ул. Кул Гали', 'Ул. Симонова', 'Ул. Карбышева']
    else:  # Пожарная сигнализация
        addresses = ['Ул. Аметьевская магистраль д 18 к 1', 'Ул. Аметьевская магистраль д 18 к 2',
                     'Ул. Аметьевская магистраль д 18 к 3', 'Ул. Аметьевская магистраль д 18 к 5', 'Ул. Седова',
                     'Ул. Кул Гали', 'Ул. Симонова', 'Ул. Карбышева']

    markup.add(*[types.KeyboardButton(address) for address in addresses])

    bot.send_message(chat_id=message.chat.id, text=f"Выберите адрес для заявки по {service}:", reply_markup=markup)


@bot.message_handler(
    regexp='Ул\. Аметьевская магистраль д 18 к 1|Ул\. Аметьевская магистраль д 18 к 2|Ул\. Аметьевская магистраль д 18 к 3|Ул\. Аметьевская магистраль д 18 к 5|Ул\. Седова|Ул\. Кул Гали|Ул\. Симонова|Ул\. Карбышева')
def address_selected(message):
    # ... остальной код функции остается без изменений
    selected_address = message.text
    user_states[message.chat.id]['address'] = selected_address

    bot.send_message(chat_id=message.chat.id, text="Укажите номер квартиры:")
    bot.register_next_step_handler(message, handle_apartment)


def handle_apartment(message):
    user_states[message.chat.id]['apartment'] = message.text

    bot.send_message(chat_id=message.chat.id, text="Укажите причину заявки и номер телефона, что бы наш специалист смог с вами связаться:")
    bot.register_next_step_handler(message, handle_reason)


def handle_reason(message):
    user_states[message.chat.id]['reason'] = message.text

    service = user_states[message.chat.id]['service']
    selected_address = user_states[message.chat.id]['address']
    apartment = user_states[message.chat.id]['apartment']
    reason = user_states[message.chat.id]['reason']
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    bot.send_message(chat_id=message.chat.id,
                     text=f"Вы выбрали адрес: {selected_address}, квартира: {apartment} для заявки по {service}. Причина: {reason}.")

    message_text = f"Новая заявка:\n\n" \
                   f"Адрес: {selected_address}\n" \
                   f"Квартира: {apartment}\n" \
                   f"Услуга: {service}\n" \
                   f"Причина: {reason}\n" \
                   f"Дата и время: {current_time}"

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(callback_data=f"complete_{message.chat.id}", text="Заявка выполнена"))

    sent_message = bot.send_message(chat_id=CHANNEL_ID, text=message_text, reply_markup=markup)

    # Сохраняем информацию о сообщении в канале и идентификатор пользователя
    user_states[sent_message.message_id] = message.chat.id

    bot.send_message(chat_id=message.chat.id, text="Заявка успешно создана. Ожидайте выполнения.")

    user_states[message.chat.id] = {}
    start(message)


@bot.callback_query_handler(func=lambda call: call.data.startswith('complete_'))
def callback_query(call):
    user_id = int(call.data.split('_')[1])

    # Получаем идентификатор пользователя по идентификатору сообщения в канале
    user_id = user_states.get(call.message.message_id)

    if user_id:
        bot.edit_message_reply_markup(chat_id=CHANNEL_ID, message_id=call.message.message_id, reply_markup=None)
        bot.send_message(chat_id=user_id, text="Ваша заявка выполнена. Спасибо за обращение!")
    else:
        bot.answer_callback_query(callback_query_id=call.id, text="Информация о заявке не найдена.")


@bot.message_handler(content_types=['text'])
def any_msg(message):
    start(message)


bot.polling(none_stop=True)