import transaction
import kombu
from pkg_resources import iter_entry_points


class MQCenter:

    __slots__ = ('emitters', 'exchanges', 'processors', 'receivers')

    def __init__(self, exchanges):
        self.exchanges = exchanges
        self.queues = {}

    def register_queue(self, exchange_name, name, routing_key="default"):
        if (exchange := in self.exchanges.get(exchange_name)) is not None:
            queue = kombu.Queue(name, exchange, routing_key)
            self.queues[name] = queue
            return queue
        raise KeyError(f'Echange {exchange_name} does not exist')


class Message:

    __slots__ = ('type', 'data')

    def __init__(self, type: str, **data):
        self.data = data
        self.type = type

    @property
    def id(self):
        return self.__hash__()

    def dump(self):
        return self.data

    @staticmethod
    def publish(payload, connection, queue, routing_key):
        exchange = queue.exchange
        with connection.Producer(serializer='json') as producer:
            producer.publish(
                payload, exchange=exchange, routing_key=routing_key,
                declare=[queue])


class MQDataManager:

    __slots__ = ('url', 'queues', 'messages')

    def __init__(self, url: str, queues: dict):
        self.url = url
        self.queues = queues
        self.messages = {}

    def createMessage(self, message: Message):
        if message.id in self.messages.keys():
            raise ValueError(f'{message.id} MessageHash already there')
        self.messages[message.id] = message

    def commit(self, transaction):
        with kombu.Connection(self.url) as conn:
            while self.messages:
                uid, message = self.messages.popitem()
                payload = message.dump()
                queue = self.queues.get(message.type)
                message.publish(payload, conn, queue, message.type)

    def abort(self, transaction):
        self.messages = {}

    def tpc_begin(self, transaction):
        pass

    def tpc_vote(self, transaction):
        pass

    def tpc_finish(self, transaction):
        pass

    def tpc_abort(self, transaction):
        pass

    def sortKey(self):
        return "~mq_datamanager"


class MQTransaction:

    def __init__(self, url: str, queues: dict, transaction_manager=None):
        self.url = url
        self.queues = queues
        if transaction_manager is None:
            transaction_manager = transaction.manager
        self.transaction_manager = transaction_manager

    def __enter__(self):
        dm = MQDataManager(self.url, self.queues)
        self.transaction_manager.join(dm)
        return dm

    def __exit__(self, type, value, traceback):
        pass
