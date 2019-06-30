use serde::Deserialize;

#[derive(Deserialize)]
pub struct User {
    pub id: i64,
    pub username: Option<String>,
    pub first_name: String,
    pub last_name: Option<String>,
}

#[derive(Deserialize)]
pub struct Chat {
    pub id: i64,
    pub username: Option<String>,
    pub first_name: Option<String>,
    pub last_name: Option<String>,
    #[serde(rename = "type")]
    pub chat_type: String,
}

#[derive(Deserialize)]
pub struct Message {
    pub date: i64,
    pub chat: Chat,
    pub message_id: i64,
    pub from: Option<User>,
    pub text: Option<String>,
    pub entities: Option<Vec<MessageEntity>>,
}

#[derive(Deserialize)]
pub struct MessageEntity {
    // Only relevant fields
    #[serde(rename = "type")]
    pub entity_type: MessageEntityType,
    pub offset: i32,
    pub length: i32,
    pub user: Option<User>,
}

#[derive(Deserialize, PartialEq)]
#[serde(rename_all = "snake_case")]
pub enum MessageEntityType {
    Mention,
    Hashtag,
    Cashtag,
    BotCommand,
    Url,
    Email,
    PhoneNumber,
    Bold,
    Italic,
    Code,
    Pre,
    TextLink,
    TextMention,
}

#[derive(Deserialize)]
pub struct InlineQuery {
    pub id: String,
    pub from: User,
    pub query: String,
    pub offset: String,
}

#[derive(Deserialize)]
pub struct TelegramUpdate {
    pub update_id: i64,
    pub message: Option<Message>,
    pub inline_query: Option<InlineQuery>,
}
