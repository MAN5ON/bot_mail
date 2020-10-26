import telebot
import smtplib
import time
import schedule

bot_mail = 'tg.bot.for.life@gmail.com'
bot_pass = 'botapi1488'
mail = ""
theme = ""
texter = ""
timer = 0

bot = telebot.TeleBot("1257099394:AAETO4TgoPzfFZgrrG5WQycqVAheA_8Def4")
info = "Добро пожаловать! \n\n" \
       "> Данный бот отправляет email сообщения с вашей почты. \n" \
       "> Введите команду '/new_message' или '/start', и следуйте указаниям бота.\n" \
       "Возможно вы не знали, но:\n\n" \
       "> Элиза (англ. ELIZA) — виртуальный собеседник, компьютерная программа Джозефа Вейценбаума, написанная им в " \
       "1966 году, которая пародирует диалог с психотерапевтом, реализуя технику активного слушания. Программа была " \
       "названа в честь Элизы Дулитл, героини из пьесы «Пигмалион» Бернарда Шоу, которую обучали языку «язык " \
       "Шекспира, Мильтона и Библии».\n"


@bot.message_handler(commands=['help'])
def helper(message):
    bot.send_message(chat_id=message.chat.id, text=info)


@bot.message_handler(commands=['new_message', 'start'])
def start(message):
    bot.send_message(chat_id=message.chat.id, text='Привет, ' +
                                                   str(message.from_user.username) + '! Введи MAIL получателя!')
    bot.register_next_step_handler(message, get_mail)


def get_mail(message):
    other_mail = message.text
    global mail
    mail = str(other_mail)
    bot.send_message(chat_id=message.chat.id, text='Введи ТЕМУ письма!')
    bot.register_next_step_handler(message, get_theme)


def get_theme(message):
    other_theme = message.text
    global theme
    theme = str(other_theme)
    bot.send_message(chat_id=message.chat.id, text='Введи ТЕКСТ письма!')
    bot.register_next_step_handler(message, get_text)


def get_text(message):
    other_text = message.text
    global texter
    texter = str(other_text)
    bot.send_message(chat_id=message.chat.id, text='Через сколько отправить письмо?\n'
                                                   ' 0.5 - через 30 минут,\n'
                                                   ' 0 - сейчас,\n'
                                                   ' 1 - через час,\n'
                                                   ' 2 - через 2 часа, \n'
                                                   ' 3.5 - через 3 часа, и т.д.')
    bot.register_next_step_handler(message, get_time)


def get_time(message):
    set_timer = message.text
    global timer
    timer = float(set_timer)
    bot.send_message(chat_id=message.chat.id, text='MAIL:   ' + mail + '\n' +
                                                   'ТЕМА:   ' + theme + '\n' +
                                                   'СООБЩЕНИЕ:   ' + texter + '\n'
                                                                              'ОТПРАВИТЬ ЧЕРЕЗ:   ' + str(
        timer) + '   ЧАСОВ\n')

    bot.send_message(chat_id=message.chat.id, text='Введённые данные корректны? Если да, то напишите - "YES".\n'
                                                   'Или введите данные заново с помощью команды /new_message')
    bot.register_next_step_handler(message, get_answer)


def get_answer(message):
    if message.text.lower() == 'yes':
        time.sleep(timer * 3600)
        BODY = "\r\n".join((
            "From: %s" % bot_mail,
            "To: %s" % mail,
            "subject: %s" % theme,
            "",
            texter
        )).encode('utf-8')
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(bot_mail, bot_pass)
        server.sendmail(bot_mail, [mail], BODY)
        server.quit()
        bot.send_message(chat_id=message.chat.id, text='Сообщение отправлено!')


bot.polling()
