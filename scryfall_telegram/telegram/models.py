from typing import List, Literal, Optional, TypedDict

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


class SendMessage(TypedDict, total=False):
    chat_id: int
    text: str
    parse_mode: Optional[PARSE_MODE]
    disable_web_page_preview: Optional[bool]


class SendPhoto(TypedDict, total=False):
    chat_id: int
    photo: str
    caption: Optional[str]
    parse_mode: Optional[PARSE_MODE]


class InputMediaPhoto(TypedDict, total=False):
    type: str
    media: str
    caption: Optional[str]
    parse_mode: Optional[PARSE_MODE]


class SendMediaGroup(TypedDict):
    chat_id: int
    media: List[InputMediaPhoto]
