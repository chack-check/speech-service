from pydantic import BaseModel


class MessageRecognizedEvent(BaseModel):
    message_id: int
    content: str


class SystemEvent(BaseModel):
    event_type: str
    included_users: list[int]
    data: str


class EventSavedFile(BaseModel):
    originalUrl: str
    originalFilename: str
    convertedUrl: str | None
    convertedFilename: str | None


class EventMessage(BaseModel):
    id: int
    senderId: int
    chatId: int
    type: str
    content: str | None
    voice: EventSavedFile | None
