import asyncio
import logging
import logging.config

from publisher import RabbitPublisher
from recognizer import Recognizer
from s3 import S3Connection
from sentry import init_sentry
from services import MessageRecognizer
from settings import LOGGING_CONFIG, settings
from subscriber import RabbitConsumer

logger = logging.getLogger("default")


async def main():
    logging.config.dictConfig(LOGGING_CONFIG)
    init_sentry()
    logger.debug("setup rabbitmq publisher...")
    publisher = RabbitPublisher(settings.rabbit_url, settings.recognition_exchange)
    await publisher.setup()
    logger.debug("setup s3 connection...")
    s3_connection = S3Connection(settings.s3_endpoint_url)
    logger.debug("setup services...")
    recognizer = Recognizer()
    service = MessageRecognizer(s3_connection, recognizer, publisher)
    logger.debug("setup rabbitmq consumer...")
    consumer = RabbitConsumer(
        settings.rabbit_url, settings.chats_exchange, settings.messages_recognition_queue_name, service
    )
    await consumer.setup()
    logger.debug("listening events...")
    await consumer.listen()


asyncio.run(main())
