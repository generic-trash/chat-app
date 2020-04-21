from base64 import b64encode
from datetime import datetime, timedelta
from os import urandom


class CSRFTokenHandler:
    def __init__(self):
        self._valid_tokens = {}

    def gentok(self):
        token = b64encode(urandom(18)).decode()
        while token in self._valid_tokens:  # Always ensure unique token
            token = b64encode(urandom(18)).decode()
        time = datetime.now() + timedelta(days=1)
        self._valid_tokens[token] = time
        return token

    def validatetok(self, tok):
        tok_tval = self._valid_tokens.get(tok)
        if tok_tval is None:
            return False
        elif datetime.now() > tok_tval:
            del self._valid_tokens[tok]
            return False
        else:
            return True