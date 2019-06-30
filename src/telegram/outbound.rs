use serde::Serialize;

#[derive(Serialize)]
pub struct SendMessage {
    pub chat_id: i64,
    pub text: String,
    pub parse_mode: Option<ParseMode>,
    pub disable_web_page_preview: Option<bool>,
}

#[derive(Serialize)]
pub enum ParseMode {
    Markdown,
    HTML,
}

#[derive(Serialize)]
pub struct AnswerInlineQuery {
    pub inline_query_id: String,
    pub results: Vec<InlineQueryResultArticle>,
}

#[derive(Serialize)]
pub struct InlineQueryResultArticle {
    #[serde(rename = "type")]
    pub query_result_type: String,
    pub id: String,
    pub title: String,
    pub input_message_content: InputTextMessageContent,
    pub url: Option<String>,
    pub description: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub thumb_url: Option<String>,
    pub hide_url: Option<bool>,
}

#[derive(Serialize)]
pub struct InputTextMessageContent {
    pub message_text: String,
    pub disable_web_page_preview: bool,
}
