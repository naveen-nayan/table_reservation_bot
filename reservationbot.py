
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
    return "enter /start to start booking\nenter /cancel to cancel booking"

def handle(msg):
    print msg
    chat_id = msg['chat']['id']
    print chat_id
    command = msg['text']
    print 'Got command: %s' % command
    if str(command) == "/help":
        bot.sendMessage(chat_id, str(help_msg()))
        return
    else:
        pass

    # if /cancel
    if str(command) == "/cancel":
        js = obj2.check_chat_status(str(chat_id))
        table_no = js.get("Table No", "None")
        if table_no != "None":
            to = js.get("email", "None")
            name = js.get("name", "None")
            table_no = js.get("Table No", "None")
            subject = "Booking Canceled"
            new_table_js = {"Available": "yes"}
            table_js, total, available, booked, booked_table, available_table = obj2.check_table_status()
            table_js[str(table_no)] = new_table_js
            print table_js
            obj2.update_table_status(table_js)
            text = "Receipt: \n\nName: {0}\nEmail: {1}\nTable Number: {2}\nCancled: {3}".format(
                name, to, table_no,  "yes")
            bot.sendMessage(chat_id, text)
            obj1.send_text_email(to=to, subject=subject, text=text)
            new_js = {str(chat_id): {"status": "Booking Canceled"}}
            obj2.update_chat_status(js=new_js)
        else:
            bot.sendMessage(chat_id, "No Booking from your id")
        return
    else:
        pass

    js = obj2.check_chat_status(str(chat_id))
    # start booking
    if str(command) == "/start":
        bot.sendMessage(chat_id, str(start_msg()))
        bot.sendMessage(chat_id, "Send us your name")
        js = {str(chat_id): {"status": "Send us your name"}}
        obj2.update_chat_status(js=js)
    # take name
    elif js.get("status", "None") == "Send us your name":
        bot.sendMessage(chat_id, "Send us your mail")
        new_js = {str(chat_id): {"status": "Send us your mail", "name" : str(command)}}
        obj2.update_chat_status(js=new_js)
    # take email
    elif js.get("status", "None") == "Send us your mail":
        emai = command
        if "@" in emai:
            table_js, total, available, booked, booked_table, available_table = obj2.check_table_status()
            available_table_no = ",".join(available_table)
            name = js.get("name", "None")
            if available == "0":
                bot.sendMessage(chat_id, "We are full Thanks")
                new_js = {str(chat_id): {"status": "We are full", "email": str(command), "name": str(name)}}
                obj2.update_chat_status(js=new_js)
                return
            msg = "Our Status:\nWe have Total {0} table \nTotal Available Table : {1} \nAvailable Table Number :{2}".format(str(total), str(len(available_table)), str(available_table_no))
            bot.sendMessage(chat_id, msg)
            bot.sendMessage(chat_id, "Send us Table No")
            new_js = {str(chat_id): {"status": "Send us Table No", "email" : str(command), "name" : str(name)}}
            obj2.update_chat_status(js=new_js)
        else:
            bot.sendMessage(chat_id, "Wrong Input\nSend us your mail")
    # Take table no
    elif js.get("status", "None") == "Send us Table No":
        table_no = str(command)
        table_js, total, available, booked, booked_table, available_table = obj2.check_table_status()
        if table_no in available_table:
            name = js.get("name", "None")
            emai = js.get("email", "None")
            text = "given details: \n\nName: {0}\nEmail: {1}\nTable Number: {2}".format(name, emai, str(command))
            bot.sendMessage(chat_id, text)
            bot.sendMessage(chat_id, "Confirm with yes")
            new_js = {str(chat_id): {"status": "Confirmation", "email": str(emai), "name": str(name), "Table No": str(command)}}
            obj2.update_chat_status(js=new_js)
        else:
            bot.sendMessage(chat_id, "Wrong input\nSend us Table No")
    # Take confirmation
    elif js.get("status", "None") == "Confirmation":
        if str(command).lower() == "yes":
            bot.sendMessage(chat_id, "Booking Confirmed")
            booking_no = int(obj2.get_booking_no())
            booked_js = {"Booking No": str(booking_no + 1)}
            obj2.updat_booking_no(booked_js)
            to = js.get("email", "None")
            name = js.get("name", "None")
            table_no = js.get("Table No", "None")
            subject = "Booking Confirmation"
            new_table_js = {"Available": "no", "mail": to, "name": name, "Confirmed": "yes", "Booking No": str(booking_no)}
            table_js, total, available, booked, booked_table, available_table = obj2.check_table_status()
            table_js[str(table_no)] = new_table_js
            print table_js
            obj2.update_table_status(table_js)
            text = "Receipt: \n\nName: {0}\nEmail: {1}\nTable Number: {2}\nBooking Number: {3}\nConfirmed: {4}".format(name, to, table_no, booking_no, "yes")
            bot.sendMessage(chat_id, text)
            obj1.send_text_email( to=to, subject=subject, text=text)
        else:
            bot.sendMessage(chat_id, "Wrong Input\nConfirm with yes")
    else:
        pass


MessageLoop(bot, handle).run_as_thread()
print 'I am listening...'

while 1:
     time.sleep(2)
