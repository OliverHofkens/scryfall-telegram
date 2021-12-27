from typing import List, Literal, Optional, TypedDict, Union

PARSE_MODE = Literal["Markdown", "HTML"]


class User(TypedDict):
    id: int
    username: Optional[str]
    first_name: str
    last_name: Optional[str]


class Chat(TypedDict):
    id: int
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    type: str


class MessageEntity(TypedDict):
    type: Literal[
        "mention",
        "hashtag",
        "cashtag",
        "bot_command",
        "url",
        "email",
        "phone_number",
        "bold",
        "italic",
        "code",
        "pre",
        "text_link",
        "text_mention",
    ]
    offset: int
    length: int
    user: Optional[User]


Message = TypedDict(
    "Message",
    {
        "date": int,
        "chat": Chat,
        "message_id": int,
        "from": User,
        "text": Optional[str],
        "entities": Optional[List[MessageEntity]],
    },
)


InlineQuery = TypedDict(
    "InlineQuery", {"id": str, "from": User, "query": str, "offset": str}
)


class TelegramUpdate(TypedDict):
    update_id: int
    message: Optional[Message]
    inline_query: Optional[InlineQuery]


class InputTextMessageContent(TypedDict):
    message_text: str
    disable_web_page_preview: bool


class InlineQueryResultArticle(TypedDict):
    type: str
    id: str
    title: str
    input_message_content: InputTextMessageContent
    url: Optional[str]
    description: Optional[str]
    thumb_url: Optional[str]
    hide_url: Optional[bool]


class AnswerInlineQuery(TypedDict):
    inline_query_id: str
    results: List[InlineQueryResultArticle]


class LoginUrl(TypedDict, total=False):
    url: str
    forward_text: Optional[str]
    bot_username: Optional[str]
    request_write_access: Optional[bool]


class InlineKeyboardButton(TypedDict, total=False):
    text: str
    url: Optional[str]
    login_url: Optional[LoginUrl]
    callback_data: Optional[str]
    switch_inline_query: Optional[str]
    switch_inline_query_current_chat: Optional[str]


class KeyboardButton(TypedDict, total=False):
    text: str
    request_contact: Optional[bool]
    request_location: Optional[bool]


class InlineKeyboardMarkup(TypedDict):
    inline_keyboard: List[List[InlineKeyboardButton]]


class ReplyKeyboardMarkup(TypedDict, total=False):
    keyboard: List[List[KeyboardButton]]
    resize_keyboard: Optional[bool]
    one_time_keyboard: Optional[bool]
    input_field_placeholder: Optional[str]
    selective: Optional[bool]


class ReplyKeyboardRemove(TypedDict, total=False):
    remove_keyboard: Literal[True]
    selective: Optional[bool]


class ForceReply(TypedDict, total=False):
    force_reply: Literal[True]
    input_field_placeholder: Optional[str]
    selective: Optional[bool]


ReplyMarkup = Union[
    InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply
]


class SendMessage(TypedDict, total=False):
    chat_id: int
    text: str
    parse_mode: Optional[PARSE_MODE]
    entities: Optional[List[MessageEntity]]
    disable_web_page_preview: Optional[bool]
    disable_notification: Optional[bool]
    reply_to_message_id: Optional[int]
    allow_sending_without_reply: Optional[bool]
    reply_markup: Optional[ReplyMarkup]


class SendPhoto(TypedDict, total=False):
    chat_id: int
    photo: str
    caption: Optional[str]
    parse_mode: Optional[PARSE_MODE]
    caption_entities: Optional[List[MessageEntity]]
    disable_notification: Optional[bool]
    reply_to_message_id: Optional[int]
    allow_sending_without_reply: Optional[bool]
    reply_markup: Optional[ReplyMarkup]


class InputMediaPhoto(TypedDict, total=False):
    type: str
    media: str
    caption: Optional[str]
    parse_mode: Optional[PARSE_MODE]


class SendMediaGroup(TypedDict):
    chat_id: int
    media: List[InputMediaPhoto]
