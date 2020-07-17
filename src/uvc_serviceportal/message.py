import json
import transaction
from dataclasses import dataclass


@dataclass
class Message:
    type: str
    body: str


class FlashMessageDataManager:

    __slots__ = ('session', 'messages', 'session_key')

    def __init__(self, session, session_key):
        self.session = session
        self.session_key = session_key
        self.messages = []

    def createMessage(self, body, type='info'):
        self.messages.append(Message(type=type, body=body))

    def consumeMessage(self):
        if messages := self.session.get(self.session_key):
            message = messages.pop()
            self.session.save()
            return message
        return None

    def exhaustMessages(self):
        if messages := self.session.get(self.session_key):
            while messages:
                yield json.loads(messages.pop())
                self.session.save()

    @property
    def hasMessages(self):
        return bool(self.session.get(self.session_key))

    def commit(self, transaction):
        if self.messages:
            messages = self.session.get(self.session_key, [])
            self.session[self.session_key] = messages + [
                json.dumps(message.__dict__) for message in self.messages]
            self.session.save()

    def abort(self, transaction):
        self.messages = []

    def tpc_begin(self, transaction):
        pass

    def tpc_vote(self, transaction):
        pass

    def tpc_finish(self, transaction):
        pass

    def tpc_abort(self, transaction):
        pass

    def sortKey(self):
        return "~flash_datamanager"


class FlashMessages:

    __slots__ = ('txn', 'session', 'session_key')

    def __init__(self, session, session_key, txn=None):
        self.session = session
        self.session_key = session_key
        if txn is None:
            txn = transaction.get()
        self.txn = txn

    def __enter__(self):
        dm = FlashMessageDataManager(self.session, self.session_key)
        self.txn.join(dm)
        return dm

    def __exit__(self, type, value, traceback):
        pass
