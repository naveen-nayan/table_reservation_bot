import os
import json
import inspect
from firebase import firebase as fb
import commands as cm


class DATAUPDATE:

    def __init__(self):
        # Device id path
        self.__dbURL = "https://table-reservation-bot.firebaseio.com"
        self.__node = "Hotel Galaxy Internation"


    def update_database(self, js):
        firebase = fb.FirebaseApplication(self.__dbURL, authentication=None)
        result = firebase.patch(self.__node, js)


    def check_status(self):
        firebase = fb.FirebaseApplication(self.__dbURL, authentication=None)
        status = firebase.get(self.__node, None)
        print status
        return status

def main():
    odj = DATAUPDATE()
    js = odj.check_status()
    odj.update_database(js)

if __name__ == "__main__":
    main()