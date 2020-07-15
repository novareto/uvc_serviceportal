import enum
import transaction
import kombu
import typing
from pkg_resources import iter_entry_points


class ExchangeType(enum.Enum):
    direct = "direct"
    topic = "topic"
    fanout = "fanout"
    headers = "headers"


class Message:

    __slots__ = ('routing_key', 'data', 'queue')

    def __init__(self, queue: str, routing_key: str, data: typing.Any):
        self.data = data
        self.queue = queue
        self.routing_key = routing_key

    @property
    def id(self):
        return self.__hash__()


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
            producer = conn.Producer(serializer='json')
            for uid, message in self.messages.items():
                queue = self.queues[message.queue]
                producer.publish(message.data,
                                 exchange=queue.exchange,
                                 routing_key=message.routing_key,
                                 declare=[queue])

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

    def __init__(self, url: str, queues: dict, txn=None):
        self.url = url
        self.queues = queues
        if txn is None:
            txn = transaction.get()
        self.txn = txn

    def __enter__(self):
        dm = MQDataManager(self.url, self.queues)
        self.txn.join(dm)
        return dm

    def __exit__(self, type, value, traceback):
        pass


class MQCenter:

    exchanges: typing.Dict
    queues: typing.Dict

    __slots__ = ('queues', 'exchanges')

    def __init__(self, exchanges=None):
        if exchanges is None:
            exchanges = {}
        self.exchanges = exchanges
        self.queues = {}

    def register_exchange(self, name: str, type: ExchangeType):
        type = ExchangeType(type)  # idempotent
        if name in self.exchanges:
            raise KeyError(f'Exchange `{name}` already exists.')
        self.exchanges[name] = kombu.Exchange(
            name, type=type.value, durable=True)
        return self.exchanges[name]

    def register_queue(self, exchange_name, name, routing_key="default"):
        if (exchange := self.exchanges.get(exchange_name)) is None:
            raise KeyError(f'Echange {exchange_name} does not exist')
        self.queues[name] = kombu.Queue(name, exchange, routing_key)
        return self.queues[name]

    def get_transaction(self, url, transaction_manager=None):
        return MQTransaction(url, self.queues, transaction_manager)
