from twilio.rest import Client

HOST_NUMBER = "8312469327"


class ClientNotif(object):
    """
    Abstraction used for handling the list of people who want text notifications
    """
    def __init__(self, username, token, mongo_client):
        self.mongo_client = mongo_client
        self.db = mongo_client['client_list']
        self.init_clients()
        self.client = Client(username, token)

    def init_clients(self, reset=False):
        CLIENTS = [{
            "name": "Chris Risley",
            "phone": 6505211067
        }]
        if reset:
            self.mongo_client.drop_database('client_list')
        for client in CLIENTS:
            self.add_client(client_name=client["name"], client_number=client["phone"])

    def send_message(self, phone_number, msg):
        message = self.client.messages.create(to=phone_number, from_=HOST_NUMBER, body=msg)

    def add_client(self, client_name, client_number):
        if self.db.client_list.find_one({'name': client_name}) is None:
            self.db.client_list.insert_one({'name': client_name, 'phone': client_number})

    def message_all(self, msg):
        clients = self.db.client_list.find()
        for client in clients:
            self.client.messages.create(to=client["phone"], from_=HOST_NUMBER, body=client["name"] + " - \n" + msg)