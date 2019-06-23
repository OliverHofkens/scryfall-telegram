use serde::Serialize;

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
    pub thumb_url: Option<String>,
    pub hide_url: Option<bool>,
}

#[derive(Serialize)]
pub struct InputTextMessageContent {
    pub message_text: String,
    pub disable_web_page_preview: bool,
}
