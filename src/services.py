from logging import getLogger

from publisher import RabbitPublisher
from recognizer import Recognizer
from s3 import S3Connection
from schemas import MessageRecognizedEvent

logger = getLogger("default")


class MessageRecognizer:

    def __init__(self, s3_connection: S3Connection, recognizer: Recognizer, publisher: RabbitPublisher):
        self._s3_connection = s3_connection
        self._recognizer = recognizer
        self._publisher = publisher

    async def recognize_message(self, message_id: int, bucket_name: str, file_url: str) -> None:
        logger.debug(f"recognizing message with {message_id=}; {bucket_name=}; {file_url=}")
        logger.debug(f"fetching file from s3")
        file = self._s3_connection.get_file(bucket_name, file_url)
        file.seek(0)
        logger.debug(f"recognizing message")
        result = self._recognizer.recognize(file)
        logger.debug(f"message {message_id=} recognized result: {result=}")
        if result:
            event = MessageRecognizedEvent(message_id=message_id, content=result)
            event_json = event.model_dump_json()
            logger.debug(f"sending message recognized event {event_json=}")
            await self._publisher.send_message(event_json.encode())
            return None

        logger.warning(f"message {message_id=} not recognized")
        return None
