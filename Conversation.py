class Conversation:
    def __init__(self, id):
        self._comments = []
        self.id = id

    def addcomment(self, comment):
        self._comments.append(comment)

    @property
    def lst(self):
        return self._comments
