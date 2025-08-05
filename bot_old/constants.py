from telebot import types
import os
import json
os.chdir(os.path.dirname(os.path.abspath(__file__)))

Global_NUMS_AVAILABLE = [obj['id'] for obj in json.load(open('OlympiadDB.json','r'))['Global_NUMS_AVAILABLE']]
MAIN_MENU = {
    'Register' : 'Регистрация',
    'Deletion' : 'Удаление данных',
    'Help' : 'Помощь',
    'Send' : 'Отправка решений',
    'Support' : 'Техподдержка'
}

SUPPORT_MENU = {
    'Back' : 'На главную',
    'RegError' : 'Ошибка регистрации',
    'DelError' : 'Ошибка при удалении данных',
    'Question' : 'Задать другой вопрос'
}

replies = {
    'Hello' : 'Привет! Тут ты можешь отправить решения задач на проверку! Но для начала **зарегистрируйся**, если еще этого не сделал) Напечатай /help для получения руководства или посмотри в меню :3.', 
    'RegisterName' : 'Отлично! Введи свое ФИО:',
    'RegisterCode' :  'Введи код администратора (**только для администраторов**, если не был выдан -- пиши 0)',
    'RegisterNickname' : 'Еще нужен никнейм для таблицы',
    'RegisterContestName' : 'И никнейм на Я.Контесте (если у тебя нет учетной записи на Я.Контесте -- можешь создать ее позже, но потребуется повторная регистрация в боте)',
    'WrongNameFormat' : 'Пожалуйста, введи данные в корректном формате',
    'NotAdmin': 'Извини, такого ключа нет в базе. Проверь, все ли правильно ты ввел. Обратись к орагнизаторам с содержанием ошибки.',
    'DeletionError': 'Произошла ошибка при удалении давнных: Данные не найдены.',
    'DefaultSupportReply' : 'Обращение направлено администрации (функция в разработке)',
    'DefaultReply' : 'Произошла ошибка, попробуй перезапустить бота командой /start, это фиксит 99.9% багов. Текст ошибки: ',
    'RegErrorReply' : 'Обращение создано. Номер: '
}

admin_keys = ['Admin000','Admin001','Admin002','Admin003']

# Главное меню из кнопок

main_menu_keyboard = types.ReplyKeyboardMarkup(row_width=3) # Инициализация
main_menu_buttons = [types.KeyboardButton(txt) for txt in set(MAIN_MENU.values())] # Создание кнопок
main_menu_keyboard.add(*main_menu_buttons) # Пуш кнопок в меню

# Меню поддержки из кнопок 

support_menu_keyboard = types.ReplyKeyboardMarkup(row_width=2) # Инициализация
support_menu_buttons = [types.KeyboardButton(txt) for txt in set(SUPPORT_MENU.values())] # Создание кнопок
support_menu_keyboard.add(*support_menu_buttons) # Пуш кнопок в меню