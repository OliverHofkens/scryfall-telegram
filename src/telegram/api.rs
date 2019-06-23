use reqwest;
use reqwest::Url;
use std::env;

use crate::telegram::inline::AnswerInlineQuery;

const BASE_URL: &str = "https://api.telegram.org/";

pub fn answer_inline_query(answer: &AnswerInlineQuery) {
    let url = format!("{}{}/answerInlineQuery", BASE_URL, make_auth());
    let endpoint = Url::parse(&url).unwrap();

    let client = reqwest::Client::new();
    let _res = client.post(endpoint).json(answer).send().unwrap();
}

fn make_auth() -> String {
    let api_key = env::var_os("TELEGRAM_BOT_TOKEN").unwrap();

    format!("bot{}", api_key.to_str().unwrap())
}
