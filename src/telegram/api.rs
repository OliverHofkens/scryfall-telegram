use reqwest;
use reqwest::Url;
use std::env;

use crate::telegram::inline::AnswerInlineQuery;
use crate::telegram::messages::SendMessage;

const BASE_URL: &str = "https://api.telegram.org/";

pub fn answer_inline_query(answer: &AnswerInlineQuery) {
    let url = format!("{}{}/answerInlineQuery", BASE_URL, make_auth());
    let endpoint = Url::parse(&url).unwrap();

    let client = reqwest::Client::new();
    let mut res = client.post(endpoint).json(answer).send().unwrap();

    if !res.status().is_success() {
        println!(
            "[ERROR] Telegram API: HTTP {}: {:?}",
            res.status(),
            res.text()
        )
    }
}

pub fn send_message(msg: &SendMessage) {
    let url = format!("{}{}/sendMessage", BASE_URL, make_auth());
    let endpoint = Url::parse(&url).unwrap();

    let client = reqwest::Client::new();
    let mut res = client.post(endpoint).json(msg).send().unwrap();

    if !res.status().is_success() {
        println!(
            "[ERROR] Telegram API: HTTP {}: {:?}",
            res.status(),
            res.text()
        )
    }
}

fn make_auth() -> String {
    let api_key = env::var_os("TELEGRAM_BOT_TOKEN").unwrap();

    format!("bot{}", api_key.to_str().unwrap())
}
