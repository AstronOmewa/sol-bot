import telebot
from telebot import types
import sqlite3
import time
import os, sys, glob
import io
from datetime import datetime
import os
import schedule 
os.chdir(os.path.dirname(os.path.abspath(__file__)))


# Инициализация бота
bot = telebot.TeleBot('7620079866:AAG64CD-bH9gHU47Jjy2lYSbcNG9aGZwQRQ')

# Константы

commands = [
    'Помощь', 'Отправить решение', 'Регистрация', 'Инфо', 'Отозвать согласие на ОПД',
      'Задания Олимпиады', 'Назад', 'Да, продолжить', 'Нет, отменить']

keyboard = types.ReplyKeyboardMarkup(row_width=3)
buttons = [types.KeyboardButton(txt) for txt in set(commands)-{'Назад', 'Да, продолжить', 'Нет, отменить'}]
keyboard.add(*buttons)

ADMINS = ['1963035629','5218273595','1298585185','1430920990']

START_TIME = datetime(2025, 7,2,10,0,0).timestamp() #or datetime(2025, XX,YY,10,0,0).timestamp()
END_TIME = datetime(2025, 8,11,20,0,0).timestamp()
OL_DUR = END_TIME - START_TIME #int(input("Olympiad duration (s): "))

starts_count = 0
NUMS = ['1.1','1.2','1.3','1.4','1.5','1.6','1.7.1','1.7.2','1.7.3','1.7.4',
        '2.1','2.2','2.3','2.4','2.5','2.6.1','2.6.2','2.6.3',
        '3.1','3.2','3.3','3.4','3.5','3.6','3.7.1', '3.7.2']

nums_available = NUMS.copy()  # Копия для отслеживания доступных задач

rem = END_TIME - time.time()

info = {
'Время начала' : time.strftime('%d.%m.%y, %H:%M по мск', time.gmtime(START_TIME+3*3600)),
'Время окончания': time.strftime('%d.%m.%y, %H:%M по мск', time.gmtime(END_TIME+3*3600)),
'Времени осталось': time.strftime('%H часов %M минут и %S секунд.',  time.gmtime(rem+3*3600))
}
  
def find_file(name, path=os.path.abspath('D:\\omewa_bots\\sol_bot'), ext = ''):
    for root, dirs, files in os.walk(path):
        files = ['.'.join(file.split('.')[:-1]) for file in files]
        if name in files:
            return os.path.join(root, name)
    return None


def update_keyboard():
    global keyboard
    keyboard = types.ReplyKeyboardMarkup(row_width=3)
    buttons = [types.KeyboardButton(txt) for txt in set(commands)-{'Назад', 'Да, продолжить', 'Нет, отменить'}]
    keyboard.add(*buttons)

# Админы могут отправлять сообщения, для этого нужно авторизоваться

@bot.message_handler(commands=['start'])
def start(message):
    global starts_count
    try:
        if starts_count < 1:
            for admin in ADMINS:
                bot.send_message(admin, f'Бот запущен, id: {message.chat.id}, usr: {message.chat.username}')
                starts_count += 1
        update_keyboard()
        
        bot.reply_to(
            message,
            'Привет! Тут ты можешь отправить решения задач на проверку! Но для начала зарегистрируйся, если еще этого не сделал) Напечатай /help для получения руководства или посмотри в меню :3.',
            reply_markup=keyboard
        )
    except e:
        print(e)
@bot.message_handler(func=lambda message: message.text in commands)
def handle_main_buttons(message):

    match message.text:
        case 'Помощь':
            help_command(message)
        case 'Отправить решение':
            if not find_file(f'{message.chat.id}_data'):
                bot.send_message(message.chat.id, 'Ой! Кажется, вы не зарегистрировались или не дали согласие на ОПД. Зарегистрируйтесь снова для отправки решений :3')
            else:
                if time.time()<START_TIME:
                    global info
                    bot.send_message(message.chat.id, 'Подожди, олимпиада начнется '+info['Время начала']+'. Можешь пока заварить себе чая :3')
                elif START_TIME<time.time()<=END_TIME:
                    send_command(message)
                else:
                    bot.send_message(message.chat.id, 'К сожалению, вы не можете отправить решение, так как время, отведенное на выполнение олипиады, истекло.')
        case 'Регистрация':
            global commands
            if message.chat.id in ADMINS:
                commands.append('Отправить сообщение участникам')
            update_keyboard()
            reg_auth_command(message)
        case 'Да, продолжить':
            bot.send_message(message.chat.id, "Введите ФИО и ник ДЛЯ ТАБЛИЦЫ через косую черту. Пример: Иванов И.И./ivanovii")
            bot.register_next_step_handler(message, reg_name)  # Ждём ввод пользователя
        case 'Нет, отменить':
            start(message)
        case 'Инфо':
            remaining = END_TIME - time.time()
            if remaining > 0:
                days = int(remaining // 86400)
                hours = int((remaining % 86400) // 3600)
                minutes = int((remaining % 3600) // 60)
                seconds = int(remaining % 60)
                
                time_parts = []
                if days > 0:
                    time_parts.append(f"{days} {'день' if str(days)[-1] == '1' else 'дня' if 2 <= int(str(days)[-1]) <= 4 else 'дней'}")
                if hours > 0:
                    time_parts.append(f"{hours} {'час' if int(str(hours)[-1]) == 1 else 'часа' if 2 <= int(str(hours)[-1]) <= 4 else 'часов'}")
                if minutes > 0:
                    time_parts.append(f"{minutes} {'минута' if int(str(minutes)[-1]) == 1 else 'минуты' if 2 <= int(str(minutes)[-1]) <= 4 else 'минут'}")
                if seconds > 0 or not time_parts:
                    time_parts.append(f"{seconds} {'секунда' if int(str(seconds)[-1]) == 1 else 'секунды' if 2 <= int(str(seconds)[-1]) <= 4 else 'секунд'}")
                
                remaining_str = ' '.join(time_parts)
            else:
                remaining_str = "00 часов 00 минут 00 секунд"
            
            info = {
                'Время начала': time.strftime('%d.%m.%Y %H:%M', time.localtime(START_TIME)),
                'Время окончания': time.strftime('%d.%m.%Y %H:%M', time.localtime(END_TIME)),
                'Времени осталось': remaining_str
            }

            bot.send_message(message.chat.id, 'Информация:\n' + '\n'.join([f'{key}: {info[key]}' for key in info]))         
        case 'Назад':
            start(message)
        case 'Отозвать согласие на ОПД':
            try:
                bot.send_message(message.chat.id, 'Успешно! Все персональные данные удалены с сервера!')
                os.remove(f'{message.chat.id}_data.txt')
                start(message)
            except:
                print('Файл не найден')
        case 'Задания Олимпиады':
            try:
                bot.send_document(message.chat.id, document=open('D:/omewa_bots/sol_bot/data/Комплект заданий.pdf','rb'))
                bot.reply_to(message, 'Успехов в решении!')
                for admin in ADMINS:
                    bot.send_message(admin, f'Был запрошен комплект заданий, id{message.chat.id}')
            except Exception as e:
                bot.reply_to(message, f'Ой, что-то пошло не так. Скопируйте содержимое сообщения и отправьте жюри.\n{str(e)}')
        case 'Назад':
            handle_back_button(message)


@bot.message_handler(commands=['regauth'])
def reg_auth_command(message):
    if not find_file(f'{message.chat.id}_data'):
        keyboard = types.ReplyKeyboardMarkup(row_width=2)
        buttons = [types.KeyboardButton('Да, продолжить'), types.KeyboardButton('Нет, отменить'), types.KeyboardButton('Назад')]
        keyboard.add(*buttons)
        
        bot.send_message(
            message.chat.id,
            'Регистрируясь, вы подтверждаете, что принимаете согласие на обработку персональных данных (ФИО, ник телеграм)',
            reply_markup=keyboard
        )
        # НЕ вызываем handle_main_buttons снова!
    else:
        bot.reply_to(message, 'Авторизация прошла успешно!')

def reg_name(message):
            usernames = [str(open(os.path.join(os.getcwd(),filename), 'r', encoding = 'utf-8').readline()).split('/')[1] for filename in glob.glob('*.txt')]
            print(usernames)
    # Обработка введённых данных (ФИО/ник)
            try:
                full_name, username = message.text.split('/')
                if username == '' or username in usernames:
                    bot.reply_to(message, 'Ник для таблицы должен быть непустым.')
                    bot.register_next_step_handler(message)   
                with open(f'{message.chat.id}_data.txt', 'w', encoding='utf-8') as f:
                    f.write(f"[{message.chat.id}] {full_name.strip()}/{username.strip()}")
                bot.reply_to(message, "Регистрация завершена!")
                start(message)  # Возвращаем в главное меню
            except Exception as e:
                bot.reply_to(message, "Ошибка! Введите данные в формате: ФИО/ник\nПример: Иванов И.И./ivanovii")
                bot.register_next_step_handler(message, reg_name)  # Повторяем запрос

@bot.message_handler(commands=['help'])
def help_command(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1)
    keyboard.add(types.KeyboardButton('Назад'))
    
    bot.reply_to(
        message,
        """Чтобы отправить решение, сначала зарегистрируйтесь. Далее напечатайте "Отправить решение" (без кавычек) или /send, далее выберите номер задания. Учтите, что учитывается только первое отправленное решение, так что при отправке на всякий случай проверьте, что все верно. Решения принимаются только в формате .pdf. Конвертировать несколько картинок в [ILovePDF](https://www.ilovepdf.com/jpg_to_pdf)""",
        reply_markup=keyboard,
        parse_mode = 'Markdown'
    )
    bot.register_next_step_handler(message, handle_back_button)

def handle_back_button(message):
    if message.text == 'Назад':
        start(message)

@bot.message_handler(commands=['send'])
def send_command(message):
    global nums_available
    usr = str(open(f'{message.chat.id}_data.txt',encoding='utf-8').readline()).split('/')[1]
    # print(usr)
    nums_available = [x for x in NUMS if not find_file(f'sol_{usr}_{x}')]
    # print(nums_available)
    if not find_file(f'sol_{message.chat.username}_{message.text}') and message.text in NUMS:
        nums_available.append(message.text)
        nums_available.sort()
    keyboard = types.ReplyKeyboardMarkup(row_width=6)
    buttons = [types.KeyboardButton(num) for num in nums_available] + [types.KeyboardButton('Назад')]
    keyboard.add(*buttons)
    if time.time()<START_TIME:
        bot.send_message(message.chat.id, 'Подожди, олимпиада начнется '+info['Время начала']+'. Можешь пока заварить себе чая :3')
        start(message)
    elif START_TIME<time.time()<=END_TIME:
        bot.reply_to(message, 'Выберите номер задачи:', reply_markup=keyboard)
        bot.register_next_step_handler(message, handle_task_selection)
    else:
        bot.send_message(message.chat.id, 'К сожалению, вы не можете отправить решение, так как время, отведенное на выполнение олипиады, истекло.')
        start(message)

def handle_task_selection(message):
    # print(message.text, find_file(f'sol_{message.chat.username}_{message.text}'))
    

    if message.text == 'Назад':
        start(message)
    elif message.text in nums_available:
        if find_file(f'sol_{message.chat.username}_{message.text}'):
            bot.reply_to(message, 'Ты уже отослал решение этой задачи. Выбери другую.')
            bot.register_next_step_handler(message, handle_task_selection)
        else:
            bot.reply_to(message, "Отлично! Теперь отправь решение в формате .pdf (можно соединить несколько картинок в 1 pdf ):")
            bot.register_next_step_handler(message, lambda m: handle_solution(m, message.text))
    else:
        bot.reply_to(message, 'Такой задачи нет(')
        bot.register_next_step_handler(message, handle_task_selection)

@bot.message_handler(content_types=['document','photo'])
def handle_solution(message, task_num):
    if message.content_type != 'document':
        bot.reply_to(message, "Отправь документ в формате pdf. Смотри инструкцию как по команде /help.")  
    elif message.content_type == 'document' and time.time()<END_TIME:
        file_id = message.document.file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        # Получаем расширение файла
        file_ext = os.path.splitext(message.document.file_name)[1]
        # print(message.chat.username, file_ext)
        try:
            filename = f"sol_{open(f'{message.chat.id}_data.txt').readline().split('/')[1]}_{task_num}.pdf"
            if file_ext!='.pdf':
                bot.reply_to(message, "Конвертируй в pdf и повтори попытку.")
            else:
                with open(filename, 'wb') as new_file:
                    new_file.write(downloaded_file)
                
                for admin in ADMINS:
                    bot.send_message(admin, f'{message.chat.id}\nРешение задачи {task_num}')
                    bot.send_document(admin, document=open(filename, 'rb'))
                
                if task_num in nums_available:
                    nums_available.remove(task_num)
        except Exception as e:
            bot.reply_to(message, f'Ой, что-то пошло не так. Отправь это сообщение жюри. \n{str(e)}')
        
        
    else:
        bot.send_message(message.chat.id, 'К сожалению, вы не можете отправить решение, так как время, отведенное на выполнение олипиады, истекло или расширение файла не соответствует нужному.')
        handle_back_button(message)

    send_command(message)

bot.polling(none_stop=True)