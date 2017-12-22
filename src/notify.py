from textmagic.rest import TextmagicRestClient
import pymongo


class ClientNotif(object):
    """
    Abstraction used for handling the list of people who want text notifications
    """

    def __init__(self, username, token, db):
        self.db = db
        self.client = TextmagicRestClient(username, token)

    def send_message(self, phone_number, msg):
        message = self.client.messages.create(phones=phone_number, text=msg)

    def add_client(self, client_name, client_number):
        self.db.client_list.insert({'name': client_name, 'phone': client_number})

    def message_all(self, msg):
        clients = self.db.client_list.find({})
        for client in clients:
            self.client.messages.create(client["phone"], msg)