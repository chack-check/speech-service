import logging

import aio_pika
from aio_pika.abc import (
    AbstractChannel,
    AbstractConnection,
    AbstractIncomingMessage,
    AbstractQueue,
)

from schemas import EventMessage, SystemEvent
from services import MessageRecognizer
from settings import settings

logger = logging.getLogger("default")


class RabbitConsumer:
    _connection: AbstractConnection | None
    _channel: AbstractChannel | None
    _queue: AbstractQueue | None

    def __init__(self, url: str, exchange_name: str, queue_name: str, service: MessageRecognizer):
        self._url = url
        self._exchange_name = exchange_name
        self._queue_name = queue_name
        self._connection = None
        self._channel = None
        self._queue = None
        self._service = service

    async def setup(self):
        self._connection = await aio_pika.connect_robust(self._url)
        self._channel = await self._connection.channel()
        self._queue = await self._channel.declare_queue(self._queue_name, durable=False)
        exchange = await self._channel.declare_exchange(self._exchange_name, aio_pika.ExchangeType.FANOUT, durable=True)
        await self._queue.bind(exchange)

    async def _handle_message(self, message: AbstractIncomingMessage) -> None:
        logger.debug(f"fetched message {message=}")
        system_event = SystemEvent.model_validate_json(message.body)
        logger.debug(f"parsed message system event: {system_event=}")
        if system_event.event_type == "message_created":
            message_data = EventMessage.model_validate_json(system_event.data)
            if message_data.type != "voice" or not message_data.voice:
                return

            logger.debug(f"handling message created event {message_data=}")
            file_url = message_data.voice.convertedUrl or message_data.voice.originalUrl
            await self._service.recognize_message(message_data.id, settings.bucket_name, file_url)

    async def listen(self):
        assert self._queue
        logger.debug("creating iterator...")
        async with self._queue.iterator() as queue_iter:
            logger.debug("iterate by messages...")
            async for message in queue_iter:
                logger.debug(f"received message {message=}")
                try:
                    await self._handle_message(message)
                except Exception as e:
                    logger.exception(e)

                await message.ack()
