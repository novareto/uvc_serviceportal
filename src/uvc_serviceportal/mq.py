import enum
import transaction
import kombu
import typing
from dataclasses import dataclass
from pkg_resources import iter_entry_points


class ExchangeType(enum.Enum):
    direct = "direct"
    topic = "topic"
    fanout = "fanout"
    headers = "headers"


@dataclass
class Message:
    data: typing.Any
    queue: str
    routing_key: str


class MQDataManager:

    __slots__ = ('url', 'queues', 'messages')

    def __init__(self, url: str, queues: dict):
        self.url = url
        self.queues = queues
        self.messages = []

    def createMessage(self, message: Message):
        if message in self.messages:
            raise ValueError(f'{message} already created.')
        if message.queue not in self.queues:
            raise KeyError(f'unknown Queue `{message.queue}`.')
        self.messages.append(message)

    def commit(self, transaction):
        with kombu.Connection(self.url) as conn:
            producer = conn.Producer(serializer='json')
            for message in self.messages:
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

    url: str
    exchanges: typing.Dict
    queues: typing.Dict

    __slots__ = ('url', 'queues', 'exchanges')

    def __init__(self, url, exchanges=None):
        self.url = url
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

    def get_transaction(self, transaction_manager=None):
        if transaction_manager is None:
            transaction_manager = transaction.get()
        return MQTransaction(self.url, self.queues, transaction_manager)
