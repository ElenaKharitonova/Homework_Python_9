import random
import telebot
from telebot import types

game_started = False
r_number = None

bot = telebot.TeleBot("TOKEN", parse_mode=None)

markup = types.ReplyKeyboardMarkup(row_width=2)
itembtn1 = types.KeyboardButton('играть')
itembtn2 = types.KeyboardButton('вычислить')
itembtn3 = types.KeyboardButton('выход')
markup.add(itembtn1, itembtn2,itembtn3) 

@bot.message_handler(commands=['start', 'help']) 
def send_welcome(message):
	bot.send_message(message.from_user.id,f"Привет, {message.from_user.first_name}",reply_markup=markup)

@bot.message_handler(content_types=['text']) 
def read_text_commands(message):
    
    global game_started
    global r_number
         
    if game_started:
        if message.text.isdigit():
            number =int(message.text)
            if number > r_number:
                bot.reply_to(message,f"Мое число меньше {number}")
            elif number < r_number:
                bot.reply_to(message,f"Мое число больше {number}")
            else:
                game_started = False
                bot.reply_to(message,f"Поздравляю! Ты угадал(а), {number} - верный ответ")
        else:
            bot.reply_to(message,'Чтобы играть, введи число цифрами. Если не хочешь играть, нажми "выход"')  
            if message.text == 'выход':   
                game_started = False
                bot.reply_to(message,'Ты вышел(ла) из игры')
            return  
       
    elif  message.text == 'играть':        
        if not game_started:
            game_started = True
            r_number = random.randint(1,1001)
            bot.reply_to(message,f"Я загадал число от 1 до 1000. Попробуй его угадать.")
        else:
            bot.reply_to(message,f"Вы уже в игре. Жду от Вас число.")

    elif  message.text == 'вычислить':
        bot.reply_to(message,f"Введи выражение. Для действий используй '*' для умножения, \
            '/' для деления, '+' или '-' для сложения и вычитания")
        bot.register_next_step_handler(message,calculate)
    
def calculate(message):
    try:
        bot.reply_to(message,f"Ответ: {eval(message.text)}")
    except NameError:
        bot.reply_to(message,f"Вы ввели выражение не верно")    
        
bot.infinity_polling()