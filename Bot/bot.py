import telebot, os
import constants
os.chdir(os.path.dirname(os.path.abspath(__file__)))

bot = telebot.TeleBot('8024003405:AAH0H-OkoZVLOFOzvFy_ap6cebk-ranFa28')

@bot.message_handler(['/start'])
def start(message):
    bot.reply_to(message, 
            constants.replies['Hello'],     
            reply_markup=constants.main_menu_keyboard,
            parse_mode = 'Markdown'
    )
    bot.register_next_step_handler(message, handle_main_menu_buttons)
    
@bot.message_handler(
    func = lambda message: message in constants.MAIN_MENU.values()
)
def handle_main_menu_buttons(message):
    pass