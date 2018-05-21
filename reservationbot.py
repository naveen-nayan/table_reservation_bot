
import time
import telepot
from mail.send_mail import SENDMAIL
from telepot.loop import MessageLoop
from database.database import DATAUPDATE

token = "577565624:AAFdDaKsq1lebLC4jruLLvX87q1fnReJ7po"
bot = telepot.Bot(token=token)
print bot.getMe()
obj1 = SENDMAIL()
obj2 = DATAUPDATE()


def start_msg():
    js = obj2.check_status()
    welcome_message = js.get("welcome msg", "None")
    return welcome_message

def help_msg():
    return "enter /start to start booking"

def take_name():

    pass

def handle(msg):
    print msg
    chat_id = msg['chat']['id']
    print chat_id
    command = msg['text']

    print 'Got command: %s' % command
    if str(command) == "/start":
        bot.sendMessage(chat_id, str(start_msg()))
        bot.sendMessage(chat_id, "Send us your name")
        js = {str(chat_id): "Send us your name"}
        obj2.update_chat_status(js=js)

    # if  old_msg == get_name:
    #     name = msg['text']
    #     bot.sendMessage(chat_id, "Send us your email")
    #     old_msg = "Send us your email"
    # if old_msg == get_mail:
    #     email = msg['text']
    #     bot.sendMessage(chat_id, "enter number of people")
    #     old_msg = "enter number of people"
    # if old_msg == get_count:
    #     no_of_people = msg['text']
    #     bot.sendMessage(chat_id, "Booking confirmed")
    #     to = 'nayansoex@gmail.com,'+ email
    #     subject = "Booking confirmed"
    #     text = "Hi {0} your booking for {1} is confirmed".format(str(name), str(no_of_people))
    #     obj1.send_text_email(to=to, subject=subject, text=text)


    if str(command) == "/help":
        bot.sendMessage(chat_id, str(help_msg()))


MessageLoop(bot, handle).run_as_thread()
print 'I am listening...'

while 1:
     time.sleep(10)
