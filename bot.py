import telebot
import random
import time
from telebot import types
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from re import *
import config


bot = telebot.TeleBot(config.TOKEN)

# Указываем какой текст мы будем ждать от бота, все остальное будет вызывать сообщение 'Данные введены неверно'
status = ["Замена аккумулятора", "Шлейф зарядки", "Контроллер питания",
          "Дисплейный модуль", "Стекло дисплейного модуля", "Задняя крышка", "Основная камера", "Фронтальная камера",
          "Стекло камеры", "Модемная часть", "Короткое замыкание", "Чистка после попадания влаги",
          "У меня другой запрос"]
 
inc_type = []  # Хранит в себе тип заявки
cli_num = []  # Хранит в себе номер телефона заявителя
cli_mail = []  # Хранит в себе почту заявителя
hello_count = []  # Хранит в себе данные о том нужно ли здороваться с пользователем

#забезпечує викнання коду навіть, якщо є якісь помилки
@bot.message_handler(commands=["test"]) #Создаем команду
def start(message):
    try: #Заворачиваем все в try
        bot.send_message(message.chat.id, "<b>Все в порядке!</b>" , parse_mode="HTML") 
        #bot.forward_message(config.owner, message.chat.id, message.message_id)
    except:
        bot.send_message(config.owner, 'Что-то пошло не так!')


@bot.message_handler(commands=['start'])
def welcome(message):
    inc_type.clear()
    cli_num.clear()
    cli_mail.clear()
    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("🛠Запрос на ремонт")
    item2 = types.KeyboardButton("✉️Связаться с нами?")
    item3= types.KeyboardButton("🌍Где нас найти")
 
    markup.add(item1, item2,item3)
    if len(hello_count) == 0:
        bot.send_message(message.chat.id, "Добрый день! {0.first_name}! \nЯ бот сервисного центра - <b>{1.first_name}</b>, Моя цель, помочь выбрать услугу по ремонту техники Apple и передать информацию о проблеме нашему сервисному инженеру!".format(message.from_user, bot.get_me()),
            parse_mode='html', reply_markup=markup)
    else:
        bot.send_message(message.chat.id,
                                 "Выберете интересующий Вас пункт меню, чтоб начать работу ".format(
                                     message.from_user, bot.get_me()),
                                 parse_mode='html', reply_markup=markup)
    hello_count.insert(1, 1)  # Отмечаем факт приветствия

@bot.message_handler(commands=["help"])
def start(message):
    if int(message.chat.id) == config.owner:
        try:
            bot.send_message(message.chat.id, 'Дополнительные команды:\n\n/test — проверяет работоспособность бота\n/id — показывает твой ID\n/send - (команда только для администраторов) каждый раз перед ответом на сообщение нужно ввести эту команду, после чего нужно ответить на желаемое сообщение.\n/start - start - если бот начал вести себя некорректно, просто нажмите на эту команду и все пройдет' )
        except:
            bot.send_message(message.chat.id, "Что-то пошло не так! Ошибка возникла в блоке кода:\n<code>@bot.message_handler(commands=['send_message'])</code>", parse_mode='HTML')
    else:
        bot.send_message(message.chat.id, 'Дополнительные команды:\n\n/test — проверяет работоспособность бота\n/id — показывает твой ID\n/start - если бот начал вести себя некорректно, просто нажмите на эту команду и все пройдет')
        bot.send_message(config.owner,'Привет, хозяин! ' + str(message.from_user.first_name) + ' использовал команду /help')
        bot.forward_message(config.owner, message.chat.id, message.message_id)

@bot.message_handler(content_types=['text'])
def statup(message):
    inc_type.clear()
    if message.chat.type == 'private':
        if message.text == '🛠Запрос на ремонт':
            key1 = types.ReplyKeyboardMarkup(True, False)
            button_phone = types.KeyboardButton(text="Отправить номер телефона", request_contact=True)
            key1.row(button_phone)
            key1.row('Ввести почту для обратной связи')
            key1.row('Ⓜ Главное меню')
            key1.one_time_keyboard = True
            if len(hello_count) == 0:  # Проверяем здоровались ли мы ранее
                bot.send_message(message.chat.id,
                                 "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, помогу тебе оформить заявку."
                                 " Отправте свой номер телефона или почту, чтоб начать работу ".format(
                                     message.from_user, bot.get_me()),
                                 parse_mode='html', reply_markup=key1)
         
            elif message.text == 'Ⓜ Главное меню':
                welcome(message)

         
            else:
                bot.send_message(message.chat.id,
                                 "Выберете средство для обратной связи, чтоб начать работу ".format(
                                     message.from_user, bot.get_me()),
                                 parse_mode='html', reply_markup=key1)
            hello_count.insert(1, 1)  # Отмечаем факт приветствия

        elif message.text == '✉️Связаться с нами?':
            bot.send_message(message.chat.id, 
                '''
Наш номер телефона:
Киевский офис    - +380*********
Харьковский офис - +380*********
                ''')
 
            key1 = types.ReplyKeyboardMarkup(True, False)
            button_phone = types.KeyboardButton(text="Отправить номер телефона", request_contact=True)
            key1.row(button_phone)
            key1.row('Ввести почту для обратной связи')
            key1.row('Online помощь')
            key1.row('Ⓜ Главное меню')
            key1.one_time_keyboard = True
            if len(hello_count) == 0:  # Проверяем здоровались ли мы ранее
                bot.send_message(message.chat.id,
                                 "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, помогу тебе оформить заявку."
                                 " Отправте свой номер телефона или почту, чтоб начать работу ".format(
                                     message.from_user, bot.get_me()),
                                 parse_mode='html', reply_markup=key1)
         
            elif message.text == 'Ⓜ Главное меню':
                welcome(message)

            elif message.text == 'Online помощь':
                bot.send_message(message.chat.id, "Соединяю с оператором")
                callback_request()

         
            else:
                bot.send_message(message.chat.id,
                                 "Выберете средство для обратной связи, чтоб начать работу ".format(
                                     message.from_user, bot.get_me()),
                                 parse_mode='html', reply_markup=key1)
            hello_count.insert(1, 1)  # Отмечаем факт приветствия
 
            

        elif message.text=='🌍Где нас найти':

            markup = types.InlineKeyboardMarkup(row_width=2)
            item4 = types.InlineKeyboardButton("Харьков", callback_data='kharkiv')
            item5 = types.InlineKeyboardButton("Киев", callback_data='kiev')

            markup.add(item4, item5)

            bot.send_message(message.chat.id, 'Виберете ваш город', reply_markup=markup)

        elif message.text == "Ввести почту для обратной связи":  # Перекидывает на ввод почты
            mail_check(message)
            if message.text == 'Ⓜ Главное меню':
                welcome(message)

        elif message.text == 'Ⓜ Главное меню':
            welcome(message)    
        else:
            #bot.send_message(message.chat.id, 'Я не знаю что ответить 😢')
            callback_request(message)
            

@bot.message_handler(content_types=["text"])           
def callback_request(message):
    if int(message.chat.id) == config.owner:
        try:
            bot.send_message(message.chat.id, 'Для отправки сообщения сделай реплей')
            bot.forward_message(config.owner, message.chat.id, message.message_id)
            bot.register_next_step_handler(message, process_mind)
            #bot.send_message(message.chat.id, 'Не верный формат отправки сообщения!!!\nИспользуйте команду команду /send \nи делайте reply на сообщения')
        except:
            bot.send_message(config.owner, 'Что-то пошло не так! Пожалуйста повторите ваш ввод! Бот продолжил свою работу.' + ' Ошибка произошла в блоке кода:\n\n <code>@bot.message_handler(content_types=["text"])</code>', parse_mode='HTML')
    else:
        pass
        try:
            bot.forward_message(config.owner, message.chat.id, message.message_id)
            #bot.send_message(message.chat.id)
        except:
            bot.send_message(config.owner, 'Что-то пошло не так!  Пожалуйста повторите ввод! Бот продолжил свою работу.')
        

@bot.message_handler(commands=['send'])
def process_start(message):
    if int(message.chat.id) == config.owner:
        try:
            bot.send_message(message.chat.id, 'Для отправки сообщения сделай реплей')
            bot.forward_message(config.owner, message.chat.id, message.message_id)
            bot.register_next_step_handler(message, process_mind)
        except:
            bot.send_message(message.chat.id, "Что-то пошло не так! Ошибка возникла в блоке кода:\n<code>@bot.message_handler(commands=['send_message'])</code>", parse_mode='HTML')
    else:
        bot.send_message(message.chat.id, 'Вы не являетесь администратором для выполнения этой команды!')


def process_mind(message):
    if int(message.chat.id) == config.owner:
        try:
            text = 'Сообщение было отправлено пользователю ' + str(message.reply_to_message.forward_from.first_name)
            bot.forward_message(message.reply_to_message.forward_from.id, config.owner, message.message_id)
            bot.send_message(config.owner, text)
        except:
            bot.send_message(message.chat.id, 'Что-то пошло не так! Пожалуйста повторите ваш ввод! Бот продолжил свою работу.' + ' Ошибка произошла в блоке кода:\n\n <code>def process_mind(message)</code>', parse_mode='HTML')
    else:
        bot.send_message(message.chat.id, 'Вы не являетесь администратором для выполнения этой команды!')

@bot.message_handler(commands=['id'])
def process_id(message):
    bot.send_message(message.chat.id, "Твой ID: " + str(message.from_user.id), parse_mode = 'HTML')
    bot.forward_message(config.owner, message.chat.id, message.message_id)


@bot.message_handler(content_types=['contact'])  # Основной обработчик
def phone_check(message):  # Уточняем у пользователя чем он с нами поделиться
    if message.text == None:  # Если пользователь нажал кнопку "Поделиться контактом" то текс будет None
        if message.contact.user_id == message.chat.id:  # Проверяем свой ли контакт дал пользователь
            cli_num.append(message.contact.phone_number)
            pre_main(message)
        else:
            bot.send_message(message.chat.id, 'Введите правильный номер телефона!')
            statup(message)
    elif message.text == 'Ⓜ Главное меню':
        welcome(message)
    else:
        statup(message)

@bot.message_handler(regexp = 'Online помощь')
def online_help(message):

    if message.text == "Online помощь":  
        bot.send_message(message.chat.id, 'Соединяю с оператором')
        process_mind(message)
    else:
        statup(message)

@bot.message_handler(regexp = 'Ⓜ Главное меню')
def menu(message):
    inc_type.clear()
    cli_num.clear()
    cli_mail.clear()
    if message.text == "Ⓜ Главное меню": 
        bot.send_message(message.chat.id, 'Вхожу в главное меню')
        welcome(message)
    else:
        statup(message)

def mail_check(message):  # Функция ввода почты
    key1 = telebot.types.ReplyKeyboardMarkup(True, False)
    key1.row("Проверить")
    bot.send_message(message.chat.id, 'Введите вашу почту ⤵')
    if message.text == 'Ввести почту для обратной связи':
        bot.register_next_step_handler(message, mail_check2)
    elif message.text == 'Ⓜ Главное меню':
        welcome(message)
 
 
def mail_check2(message):  # Проверка потчы на валидность
    pattern = compile('(^|\s)[-a-z0-9_.]+@([-a-z0-9]+\.)+[a-z]{2,6}(\s|$)')  # Проверяем совпадает ли паттерк
    is_valid = pattern.match(message.text)
    if is_valid:
        cli_mail.append(message.text)  # Записываем полученную почту
        pre_main(message)
    elif message.text == 'Ⓜ Главное меню':
        welcome(message)
    else:
        bot.send_message(message.chat.id, "Почта введена неверно.")
        statup(message)
 
 
def pre_main(message):  # Основная функция
    inc_type.clear()  # Очищаем словарь с типом заявки
    key = types.ReplyKeyboardMarkup(True, False)
    key.row('Корпусные поломки')
    key.row('Пайка', "У меня другой запрос")
    key.one_time_keyboard = True
    try:  # Спрашиваем что за инцент
        bot.send_message(message.chat.id,
                         "Итак, {0.first_name}!, что у вас случилось?.".format(
                             message.from_user, bot.get_me()),
                         parse_mode='html', reply_markup=key)
        print('No problem detected. Message send')
    except OSError:  # Спрашиваем что за инцент если предидущий вызвал ошибку таймаута
        print("ConnectionError - Sending again after 5 seconds!!!")
        time.sleep(5)
        bot.send_message(message.chat.id,
                         "Итак, {0.first_name}, что у вас случилось?.".format(
                             message.from_user, bot.get_me()),
                         parse_mode='html', reply_markup=key)
        print('Problem solved')
    bot.register_next_step_handler(message, main)
 
 
def main(message):  # Определяем тип инцидента и уточняем его подтип
    if message.text == 'Корпусные поломки':
        keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
        keyboard.row('Питание')
        keyboard.row('Дисплей и корпус')
        keyboard.row('Камера')
        keyboard.row('Ⓜ Главное меню')
        bot.send_message(message.chat.id, 'Выберите действие ⤵', reply_markup=keyboard)
        bot.register_next_step_handler(message, incedent)
    elif message.text == 'Пайка':
        keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
        keyboard.row('Модемная часть', 'Короткое замыкание')
        keyboard.row('Чистка после попадания влаги')
        keyboard.row('Ⓜ Главное меню')
        keyboard.one_time_keyboard = True
        bot.send_message(message.chat.id, 'Выберите действие ⤵', reply_markup=keyboard)
        bot.register_next_step_handler(message, info)
    elif message.text == 'У меня другой запрос':
        task = message.text
        vvod(message)
    elif message.text == 'Ⓜ Главное меню':
        welcome(message)
 
    else:
        bot.send_message(message.chat.id, '🚫 Данные введены неверно 🚫')
        pre_main(message)
 
 
def incedent(message):  # Обрабатываем подтип инцедента
    keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
    keyboard.add('Ⓜ Главное меню')
 
    if message.text == 'Питание':
        keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
        keyboard.row('Замена аккумулятора')
        keyboard.row('Шлейф зарядки')
        keyboard.row('Контроллер питания')
        keyboard.add('Ⓜ Главное меню')
        keyboard.one_time_keyboard = True
        bot.send_message(message.chat.id, 'Укажите вашу проблему ⤵', reply_markup=keyboard)
        bot.register_next_step_handler(message, vvod)
 
    elif message.text == 'Дисплей и корпус':
        keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
        keyboard.row('Дисплейный модуль')
        keyboard.row('Стекло дисплейного модуля')
        keyboard.row('Задняя крышка')
        keyboard.add('Ⓜ Главное меню')
        keyboard.one_time_keyboard = True
        bot.send_message(message.chat.id, 'Укажите вашу проблему ⤵', reply_markup=keyboard)
        bot.register_next_step_handler(message, vvod)
 
    elif message.text == 'Камера':
        keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
        keyboard.row('Основная камера')
        keyboard.row('Фронтальная камера')
        keyboard.row('Стекло камеры')
        keyboard.add('Ⓜ Главное меню')
        keyboard.one_time_keyboard = True
        bot.send_message(message.chat.id, 'Укажите вашу проблему ⤵', reply_markup=keyboard)
        bot.register_next_step_handler(message, vvod)
 
    elif message.text == 'Ⓜ Главное меню':
        welcome(message)
 
    else:
        bot.send_message(message.chat.id, 'Данные введены неверно 😢')
        pre_main(message)
 
 
def info(message):  # Обработываем подтип запроса информации
    if message.text == 'Ⓜ Главное меню':
        welcome(message)
    elif message.text == 'Модемная часть':
        global task
        task = message.text
        vvod(message)
    elif message.text == 'Короткое замыкание':
        task = message.text
        vvod(message)
    elif message.text == 'Чистка после попадания влаги':
        task = message.text
        vvod(message)
    else:
        text(message)
        bot.send_message(message.chat.id, 'Данные введены неверно')
        pre_main(message)
 
 
def vvod(message):  # Запрашиваем дополнительную информацию
    inc_type.append(message.text)
    global task
    if message.text in status:
        task = message.text
        bot.send_message(message.chat.id, 'Введите детали вашего запроса в строку ввода 😊')
        bot.register_next_step_handler(message, text)
    else:
        bot.send_message(message.chat.id, 'Данные введены неверно')
        pre_main(message)
 
 
def text(message):  # Отправляем письмо
    if message.text == 'Ⓜ Главное меню':
        welcome(message)
    else:
        keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
        keyboard.row('Ⓜ Главное меню')
        bot.send_message(message.chat.id, 'Ваш запрос \"' + message.text +
                         '\" получен. Можете вернуться в главное меню ⤵', reply_markup=keyboard)
        '''addr_from = "mail1@gmail.com"
        addr_to = "mail2@mail.ru"
        password = "password_mail1"
        msg = MIMEMultipart()  # Создаем сообщение
        msg['From'] = addr_from
        msg['To'] = addr_to
        msg['Subject'] = (message.text)'''
        body = (f'''
*Автор заявки: * {message.from_user.first_name};
 
*Телефон: * {cli_num};
 
*Тип заявки: * {inc_type};
 
*Текст заявки: * {message.text};

*Почта: * - {cli_mail}.
      ''')
        '''msg.attach(MIMEText(body, 'plain'))  # Добавляем в сообщение текст
        smtpObj = smtplib.SMTP('smtp.gmail.com', 465)  # Создаем объект SMTP
        smtpObj.starttls()  # Начинаем шифрованный обмен по TLS
        smtpObj.login(addr_from, password)  # Получаем доступ
        smtpObj.send_message(msg)  # Отправляем сообщение
        smtpObj.quit()  # Выходим'''
        bot.send_message(config.owner_chanal, str(message.from_user.id) + ": " + str(message.from_user.first_name) + ' : ' + message.text + body, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:            
            if call.data == 'kharkiv':
                markup = types.InlineKeyboardMarkup(row_width=1)
                item8 = types.InlineKeyboardButton("Показать на карте", url='https://goo.gl/maps/dHuhDU1jPPrin9uk9')

                markup.add(item8)

                bot.send_message(call.message.chat.id, "Ремонт техники Apple в Харькове с понедельника по п'ятницу с  9.00 до 18.00 и в субботу и в воскресение с 10.00 до 16.00 ул. Иванова, 5", reply_markup=markup)
            elif call.data == 'kiev':
                markup = types.InlineKeyboardMarkup(row_width=2)
                item6 = types.InlineKeyboardButton("м. Золотые Ворота", callback_data='zoloti_vorota')
                item7 = types.InlineKeyboardButton("м. Лыбедская", callback_data='libidska')

                markup.add(item6, item7)

                bot.send_message(call.message.chat.id, 'Виберете ближайший магазин', reply_markup=markup)

            elif call.data == 'zoloti_vorota':
                markup = types.InlineKeyboardMarkup(row_width=1)
                item8 = types.InlineKeyboardButton("Показать на карте", url='https://goo.gl/maps/dHuhDU1jPPrin9uk9')

                markup.add(item8)

                bot.send_message(call.message.chat.id, "Ремонт техники Apple возле метро Золотые Ворота с понедельника по п'ятницу с  10.00 до 19.00 и в субботу и в воскресение с 10.00 до 16.00 ул. Иванова, 5", reply_markup=markup)
            elif call.data =='libidska':
                markup = types.InlineKeyboardMarkup(row_width=1)
                item9 = types.InlineKeyboardButton("Показать на карте", url='https://goo.gl/maps/dHuhDU1jPPrin9uk9')

                markup.add(item9)

                bot.send_message(call.message.chat.id, "Ремонт техники Apple возле метро Лыбедская с понедельника по п'ятницу с  10.00 до 19.00 и в субботу и в воскресение с 10.00 до 16.00 ул. Иванова, 5",  reply_markup=markup)



        



 
            # remove inline buttons
            #bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="тут має бути текст, який можна видалити з інлайнових клавіатур?",
                #reply_markup=None)
 
            # show alert
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                text="Apple_bot")
 
    except Exception as e:
        print(repr(e))
 
# RUN
while True:  # Запускаем бота
    try:
        bot.polling(none_stop=True)
    except OSError:
        bot.polling(none_stop=True)

