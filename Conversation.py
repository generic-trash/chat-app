class Conversation:
    def __init__(self):
        self._comments = []

    def addcomment(self,comment):
        self._comments.append(comment)

    @property
    def lst(self):
        return self._comments