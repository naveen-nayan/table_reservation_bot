
from firebase import firebase as fb

class DATAUPDATE:

    def __init__(self):
        self.__dbURL = "https://table-reservation-bot.firebaseio.com"
        self.__node = "Hotel Galaxy Internation"


    def update_database(self, js):
        firebase = fb.FirebaseApplication(self.__dbURL, authentication=None)
        result = firebase.patch(self.__node, js)

    def update_chat_status(self, js):
        firebase = fb.FirebaseApplication(self.__dbURL, authentication=None)
        result = firebase.patch(self.__node, js)
        pass

    def check_chat_status(self, node):
        firebase = fb.FirebaseApplication(self.__dbURL, authentication=None)
        status = firebase.get(self.__node + "/"+ str(node), None)
        print status
        return status

    def check_status(self):
        firebase = fb.FirebaseApplication(self.__dbURL, authentication=None)
        status = firebase.get(self.__node, None)
        print status
        return status

    def check_table_status(self):
        available_table = []
        booked_table = []
        firebase = fb.FirebaseApplication(self.__dbURL, authentication=None)
        status = firebase.get(self.__node, "Table")
        available = status.get("Available", "None")
        booked = status.get("Booked", "None")
        total = status.get("Total", "None")
        print status
        for i in range(1, 7):
            tableno = str(i)
            js = status[tableno]
            if js.get("Available", "None") == "yes":
                available_table.append(tableno)
            elif js.get("Available", "None") == "no":
                booked_table.append(tableno)
        print status, total, available, booked, booked_table, available_table
        return status,total, available, booked, booked_table, available_table

    def update_table_status(self, js):
        firebase = fb.FirebaseApplication(self.__dbURL, authentication=None)
        result = firebase.patch(self.__node + "/Table", js)
        pass

    def get_booking_no(self):
        firebase = fb.FirebaseApplication(self.__dbURL, authentication=None)
        status = firebase.get(self.__node, "Booking No")
        return status

    def updat_booking_no(self, js):
        firebase = fb.FirebaseApplication(self.__dbURL, authentication=None)
        result = firebase.patch(self.__node, js)

def main():
    odj = DATAUPDATE()
    # js = odj.check_status()
    # odj.update_database(js)
    odj.check_table_status()

if __name__ == "__main__":
    main()