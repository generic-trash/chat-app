from UserDataHandler import UserConversationManager
from Conversation import Conversation


class DataHandler:
    def __init__(self):
        self._users = {}

    def adduser(self, user):
        self._users[user] = UserConversationManager(user)

    def add_conversation(self, user1, user2, name):
        conversation = Conversation()
        self._users[user1].add_conversation(name, conversation)
        self._users[user2].add_conversation(name, conversation)

    def user_conversation_add_comment(self, user, conversation, comment):
        self._users[user].conversation_add_comment(comment, conversation)

    def user_get_conversation(self,user,conversation):
        self._users[user].get_conversation(conversation)