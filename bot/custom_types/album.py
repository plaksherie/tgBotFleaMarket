from typing import Union, Optional, List, cast, Dict, Type, Tuple

from aiogram import Bot
from aiogram.methods import SendMediaGroup
from aiogram.types import PhotoSize, Video, Audio, Document, TelegramObject, Message, InputMediaPhoto, \
    InputMediaVideo, InputMediaAudio, InputMediaDocument, MessageEntity
from aiogram.types.base import UNSET_PROTECT_CONTENT
from pydantic import Field

Media = Union[PhotoSize, Video, Audio, Document]

INPUT_TYPES: Dict[str, Type[Union[InputMediaAudio, InputMediaDocument, InputMediaPhoto, InputMediaVideo]]] = {
    "photo": InputMediaPhoto,
    "video": InputMediaVideo,
    "audio": InputMediaAudio,
    "document": InputMediaDocument,
}


class Album(TelegramObject):
    photo: Optional[List[PhotoSize]] = None
    video: Optional[List[Video]] = None
    audio: Optional[List[Audio]] = None
    document: Optional[List[Document]] = None
    captions: List[str] = []
    messages: List[Message] = Field(default_factory=list)

    @property
    def media_types(self) -> List[str]:
        return [media_type for media_type in INPUT_TYPES if getattr(self, media_type)]

    @property
    def as_media_group(self) -> List[Union[InputMediaAudio, InputMediaDocument, InputMediaPhoto, InputMediaVideo]]:
        bot = cast(Bot, self.bot)

        group = [
            INPUT_TYPES[media_type](media=media.file_id, parse_mode=bot.parse_mode)
            for media_type in self.media_types
            for media in getattr(self, media_type)
        ]
        if group:
            group[0].caption = self.caption
        return group

    def copy_to(
        self,
        chat_id: Union[int, str],
        message_thread_id: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = UNSET_PROTECT_CONTENT,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
    ) -> SendMediaGroup:
        return SendMediaGroup(
            chat_id=chat_id,
            media=self.as_media_group,
            message_thread_id=message_thread_id,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
        ).as_(self._bot)

    def get_caption_and_entities(
            self,
    ) -> Optional[Tuple[str, List[MessageEntity]]]:
        first_message = self.messages[0]
        caption = first_message.caption
        if not caption:
            first_non_empty = next((s for s in self.captions if s), None)
            if first_non_empty:
                caption = first_non_empty
            else:
                return None
        return caption, first_message.caption_entities or []
