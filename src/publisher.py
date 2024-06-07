import aio_pika
from aio_pika.abc import AbstractChannel, AbstractConnection, AbstractExchange


class RabbitPublisher:
    _connection: AbstractConnection | None
    _channel: AbstractChannel | None
    _exchange: AbstractExchange | None

    def __init__(self, url: str, exchange_name: str):
        self._url = url
        self._exchange_name = exchange_name

    async def setup(self):
        self._connection = await aio_pika.connect_robust(self._url)
        self._channel = await self._connection.channel()
        self._exchange = await self._channel.declare_exchange(
            self._exchange_name, aio_pika.ExchangeType.FANOUT, durable=True
        )

    async def send_message(self, message: bytes):
        assert self._exchange
        await self._exchange.publish(
            aio_pika.Message(body=message, content_type="application/json"), routing_key="", timeout=2
        )
