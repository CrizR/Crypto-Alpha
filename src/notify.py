from twilio.rest import Client

HOST_NUMBER = "8312469327"

class ClientNotif(object):
    """
    Abstraction used for handling the list of people who want text notifications
    """

    def __init__(self, username, token, mongo_client):
        self.db = mongo_client['client_list']
        self.client = Client(username, token)

    def send_message(self, phone_number, msg):
        message = self.client.messages.create(to=phone_number, from_=HOST_NUMBER, body=msg)

    def add_client(self, client_name, client_number):
        self.db.client_list.insert_one({'name': client_name, 'phone': client_number})

    def message_all(self, msg):
        clients = self.db.client_list.find({})
        for client in clients:
            self.client.messages.create(client["phone"], msg)