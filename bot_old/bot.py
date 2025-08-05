import telebot
from telebot import types
import sqlite3
import time
import os, sys, glob, json, ast
from datetime import datetime
import constants, user, admin, functions, ticket


os.chdir(os.path.dirname(os.path.abspath(__file__)))

USR = None

bot = telebot.TeleBot('8024003405:AAH0H-OkoZVLOFOzvFy_ap6cebk-ranFa28') # Инициализация бота

# Обработка команд без слешей

@bot.message_handler(
        func = lambda message: message in list(constants.MAIN_MENU.values())\
            # +list(constants.SUPPORT_MENU.values())
)
def handle_main_menu_buttons(message):
    try:
        obj = functions.search_user(message.chat.id)
        global USR
        USR = user.User(
                uid=obj['uid'],
                available_nums=obj['available_nums'],
                registered=obj['registered'],
                nickname=obj['nickname'],
                yaContestName=obj['yaContestName'],
                name=obj['name'])
        if obj['is_admin']:
            USR = admin.Admin(
                uid=obj['uid'],
                available_nums=obj['available_nums'],
                registered=obj['registered'],
                nickname=obj['nickname'],
                activation_key=obj['adminKey'],
                yaContestName=obj['yaContestName'],
                name=obj['name'])
    except IndexError as e:
        USR = user.User(constants.Global_NUMS_AVAILABLE, False, None, message.chat.id, False)
        
    if message.text == constants.MAIN_MENU['Register']:
        reg(message)
    if message.text == constants.MAIN_MENU['Deletion']:
        delete(message)
    if message.text == constants.MAIN_MENU['Support']:
        bot.send_message(USR.uid, 'Что тебя интересует?', reply_markup=constants.support_menu_keyboard)
        bot.register_next_step_handler(message, handle_support_menu_buttons)
    if message.text == constants.SUPPORT_MENU['Back']: # Возврат на главную с всех меню 
        start(message)




# Приветствие + главное меню из кнопок

@bot.message_handler(commands=['start'])
def start(message):
    # Тут создаем объект пользователя, чтобы дальше было удобнее

    global USR
    USR = user.User(constants.Global_NUMS_AVAILABLE, False, None, message.chat.id, False)
    

    bot.reply_to(message, 
            constants.replies['Hello'],     
            reply_markup=constants.main_menu_keyboard,
            parse_mode = 'Markdown'
    )
    bot.register_next_step_handler(message, handle_main_menu_buttons)

# Регистрация

user_string = []

@bot.message_handler(['reg_auth'])
def reg(message):
    
    global USR
    
    try:
        if functions.search_user(USR.uid):
            rep = bot.reply_to(message, 'Авторизация прошла успешно. Для изменения данных можно удалить свои данные с сервера и пройти регистрацию заново.', parse_mode = 'Markdown')
            bot.register_next_step_handler(rep, handle_main_menu_buttons)
        else:
            rep = bot.reply_to(message, constants.replies['RegisterName'], parse_mode = 'Markdown')
            bot.register_next_step_handler(rep, process_name_step)
    except IndexError as e:
        rep = bot.reply_to(message, constants.replies['RegisterName'], parse_mode = 'Markdown')
        bot.register_next_step_handler(rep, process_name_step)

def process_name_step(message):
    global USR
    USR.name = message.text
    
    rep = bot.reply_to(message, constants.replies['RegisterCode'], parse_mode = 'Markdown')
    bot.register_next_step_handler(rep, process_code_step)
    
def process_code_step(message):
    
    is_admin, adminKey = functions.process_key(message.text)
    
    if is_admin:
        USR = admin.Admin(USR.available_nums, USR.registered, USR.name, USR.nickname, USR.uid, True, adminKey, USR.yaContestName)
    
    rep = bot.reply_to(message, constants.replies['RegisterNickname'], parse_mode = 'Markdown')
    bot.register_next_step_handler(rep, process_nickname_step)

def process_nickname_step(message):
    global user_string
    user_string += [message.text]
    
    rep = bot.reply_to(message, constants.replies['RegisterContestName'], parse_mode = 'Markdown')
    bot.register_next_step_handler(rep, process_contestName_step)
    
def process_contestName_step(message):
    
    global USR, user_string
    
    user_string += [message.text]
    print(user_string)
    try:
        name, nickname, yaContestName = user_string[0], user_string[2], user_string[3] 
        isadmin, adminKey = functions.process_key(user_string[1])
        user_string = []
        
        if isadmin:
            USR = admin.Admin(available_nums=constants.Global_NUMS_AVAILABLE, registered=True, name=name,nickname=nickname, uid = message.chat.id, activation_key=adminKey, yaContestName=yaContestName)
        else: 
            USR = user.User(available_nums=constants.Global_NUMS_AVAILABLE, registered= True, name = name, nickname=nickname, uid=message.chat.id, is_admin = False, yaContestName=yaContestName)
        respond =  USR.register()
        rep = bot.reply_to(message, respond)
        bot.register_next_step_handler(rep, handle_main_menu_buttons)
        
    except Exception as e:
        if message.text not in constants.MAIN_MENU.values():
            name = bot.send_message(USR.uid, constants.replies['WrongNameFormat']+f"\n{e}")
            bot.register_next_step_handler(name, reg)
        else:
            handle_main_menu_buttons(message)



@bot.message_handler(['delete'])
def delete(message):
    respond = ''
    try:
        respond = USR.delete()
    except Exception as e:
        respond = constants.replies['DeletionError']
    rep = bot.reply_to(message, respond)
    bot.register_next_step_handler(rep, handle_main_menu_buttons)

# Техподдержка

@bot.message_handler(func = lambda message: message in constants.SUPPORT_MENU.values())
def handle_support_menu_buttons(message):
    
    global USR     
    try:
        if message.text == constants.SUPPORT_MENU['Back']: # Возврат на главную с меню ТП
            bot.send_message(USR.uid, 'Введи команду из меню:')
            start(message)
        if message.text == constants.SUPPORT_MENU['Question']:
            rep = bot.reply_to(message, 'Введи текст обращения:')
            bot.register_next_step_handler(rep, handle_support_question)
        if message.text == constants.SUPPORT_MENU['RegError']:
            t = ticket.Ticket('latest', USR.uid, {}, 'Открыт')
            t.push_question({
                'Q1' : f'Ошибка регистрации, uid: {USR.uid}'
                })
            
            bot.reply_to(message, constants.replies['RegErrorReply'])
            bot.register_next_step_handler(handle_support_menu_buttons)
        if message.text == constants.SUPPORT_MENU['DelError']:
            bot.reply_to(message, constants.SUPPORT_MENU['DefaultSupportReply'])
    except Exception as e:
        tb = sys.exception().__traceback__
        bot.send_message(USR.uid, constants.replies['DefaultReply']+f'{e}')

def handle_support_question(message):
    global USR
    
    ticket_num = functions.get_latest_ticket_num() + 1

    id, uid, chat_history, status = ticket_num, USR.uid, {}, 'Открыто'

    for admin in functions.admins_list():
        print(USR.name)
        bot.send_message(int(admin), f'Получено новое обращение #{ticket_num}!\nName : {USR.name.decode('utf-8')}\n \
                        Nickname: {ast.literal_eval(USR.nickname).decode('utf-8')}\n\
                        {USR.uid}\n\
                        Текст обращения : \n \n_{message.text}_ \n \nСвайпни для ответа.',
                        parse_mode='Markdown')
        
        print(admin, end = ',')
    print()

    t = ticket.Ticket(id=id, uid=uid, chat_history=chat_history, status=status)
    t.status = 'Открыт'
    t.push_question({
        "id" : 'latest',
        "text" : f"_{message.text}_"
    })

    rep = bot.reply_to(message, f'Обращение #{ticket_num} успешно отправлено!\nСтатус обращения: {status}')
    bot.register_next_step_handler(rep, handle_support_menu_buttons)



bot.polling(none_stop=True)