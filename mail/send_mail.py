__author__ = 'naveen'

import smtplib


class SENDMAIL:

    def __init__(self):
        self.gmail_user = 'table.reservation.bot@gmail.com'
        self.gmail_pwd = "table_reservation"

    '''
    ##################################################################################################################
                                                    send test message
    ##################################################################################################################
    '''
    # This method is used to send mail
    def send_text_email(self, to='nayansoex@gmail.com', subject='sent from bot', text='sent from bot'):
        FROM = self.gmail_user
        TO = to.split(',')
        SUBJECT = subject
        TEXT = text

        # Prepare actual message
        message = """\From: %s\nTo: %s\nSubject: %s\n\n%s""" % (FROM, ", ".join(TO), SUBJECT, TEXT)
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.ehlo()
            server.starttls()
            server.login(self.gmail_user, self.gmail_pwd)
            server.sendmail(FROM, TO, message)
            server.close()
            print ('successfully sent the mail to : ', TO)
        except Exception as e:
            print ("failed to send mail", e)
