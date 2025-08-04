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
        func = lambda message: message in list(constants.MAIN_MENU.values())+list(constants.SUPPORT_MENU.values())
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
        rep = bot.send_message(USR.uid, 'Что тебя интересует?', reply_markup=constants.support_menu_keyboard)
        bot.register_next_step_handler(rep, handle_support_menu_buttons)
    if message.text == constants.SUPPORT_MENU['Back']: # Возврат на главную с меню ТП
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

@bot.message_handler(['reg_auth'])
def reg(message):
    bot.reply_to(message, constants.replies['Register'], parse_mode = 'Markdown')
    bot.register_next_step_handler(message, reg_name)



def reg_name(message):
    global USR
    try:
        name, isadmin, nickname, yaContestName, adminKey = functions.parse(message.text)
        if isadmin:
            USR = admin.Admin(available_nums=constants.Global_NUMS_AVAILABLE, registered=True, name=name,nickname=nickname, uid = message.chat.id, activation_key=adminKey, yaContestName=yaContestName)
        else: 
            USR = user.User(available_nums=constants.Global_NUMS_AVAILABLE, registered= True, name = name, nickname=nickname, uid=message.chat.id, is_admin = False, yaContestName=yaContestName)
        respond =  USR.register()
        bot.reply_to(message, respond)
        
    except Exception as e:
        if message.text not in constants.MAIN_MENU.values():
            bot.send_message(USR.uid, constants.replies['WrongNameFormat'])
            bot.register_next_step_handler(message, reg_name)
        else:
            handle_main_menu_buttons(message)


@bot.message_handler(['delete'])
def delete(message):
    respond = ''
    try:
        respond = USR.delete()
        bot.reply_to(message, respond)
    except Exception as e:
        print(e)
        respond = constants.replies['DeletionError']
        bot.reply_to(message, respond)


# Техподдержка

@bot.message_handler(func = lambda message: message in constants.SUPPORT_MENU.values())
def handle_support_menu_buttons(message):
    if message.text == constants.SUPPORT_MENU['Back']:
        start(message)
    if message.text == constants.SUPPORT_MENU['Question']:
        bot.reply_to(message, 'Введи текст обращения:')
        bot.register_next_step_handler(message, handle_support_question)
    if message.text == constants.SUPPORT_MENU['RegError']:
        bot.reply_to(message, constants.SUPPORT_MENU['DefaultSupportReply'])
    if message.text == constants.SUPPORT_MENU['DelError']:
        bot.reply_to(message, constants.SUPPORT_MENU['DefaultSupportReply'])

def handle_support_question(message):
    global USR
    ticket_num = functions.get_latest_ticket_num() + 1

    id, uid, chat_history, status = ticket_num, USR.uid, {}, 'Открыто'

    for admin in functions.admins_list():
        print(USR.name)
        bot.send_message(int(admin), f'Получено новое обращение #{ticket_num}!\nName : {ast.literal_eval(USR.name).decode('utf-8')}\n \
                         Nickname: {ast.literal_eval(USR.nickname).decode('utf-8')}\n\
                        {USR.uid}\n\
                        Текст обращения : \n \n_{message.text}_ \n \nСвайпни для ответа.',
                        parse_mode='Markdown')
        
        print(admin, end = ',')
    print()

    t = ticket.Ticket(id=id, uid=uid, chat_history=chat_history, status=status)
    t.status = 'Открыт'
    t.push_question({
        id:1,
        "text": f"_{message.text}_"
    })

    rep = bot.reply_to(message, f'Обращение #{ticket_num} успешно отправлено!\nСтатус обращения: {status}')
    bot.register_next_step_handler(rep, handle_support_menu_buttons)

bot.polling(none_stop=True)