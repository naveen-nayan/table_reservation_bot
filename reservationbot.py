
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
    js = obj2.check_chat_status(str(chat_id))
    if str(command) == "/start":
        bot.sendMessage(chat_id, str(start_msg()))
        bot.sendMessage(chat_id, "Send us your name")
        js = {str(chat_id): {"status": "Send us your name"}}
        obj2.update_chat_status(js=js)

    elif js.get("status", "None") == "Send us your name":
        bot.sendMessage(chat_id, "Send us your mail")
        new_js = {str(chat_id): {"status": "Send us your mail", "name" : str(command)}}
        obj2.update_chat_status(js=new_js)

    elif js.get("status", "None") == "Send us your mail":
        bot.sendMessage(chat_id, "Send us number of people")
        name = js.get("name", "None")
        new_js = {str(chat_id): {"status": "Send us no of people", "email" : str(command), "name" : str(name)}}
        obj2.update_chat_status(js=new_js)

    elif js.get("status", "None") == "Send us no of people":
        bot.sendMessage(chat_id, "Confirm with yes")
        name = js.get("name", "None")
        emai = js.get("email", "None")
        new_js = {str(chat_id): {"status": "Confirmation", "email": str(emai), "name": str(name), "No of people": str(command)}}
        obj2.update_chat_status(js=new_js)

    elif js.get("status", "None") == "Confirmation":
        if str(command).lower() == "yes":
            bot.sendMessage(chat_id, "Booking Confirmed")
            to = js.get("email", "None")
            name = js.get("name", "None")
            no_of_people = js.get("No of people", "None")
            subject = "Booking Confirmation"
            text = "Hi {0} your booking for {1} is confirmed".format(name, no_of_people)
            obj1.send_text_email( to=to, subject=subject, text=text)

    if str(command) == "/help":
        bot.sendMessage(chat_id, str(help_msg()))


MessageLoop(bot, handle).run_as_thread()
print 'I am listening...'

while 1:
     time.sleep(2)
