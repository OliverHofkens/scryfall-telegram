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
pub struct TextMessage {
    pub date: i64,
    pub chat: Chat,
    pub message_id: i64,
    pub from: Option<User>,
    pub text: Option<String>,
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
    pub message: Option<TextMessage>,
    pub inline_query: Option<InlineQuery>,
}
