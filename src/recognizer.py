from logging import getLogger
from typing import IO

import whisper

logger = getLogger("default")


class Recognizer:

    def __init__(self):
        self._model = whisper.load_model("base")

    def recognize(self, file: IO) -> str | None:
        try:
            result = self._model.transcribe(file.name, fp16=False)
            if isinstance(result["text"], list):
                return result["text"][0]

            return result["text"]
        except Exception as e:
            logger.exception(e)
            return None
