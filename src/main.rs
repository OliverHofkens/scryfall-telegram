use std::error::Error;

use lambda_http::{lambda, Body, IntoResponse, Request, Response};
use lambda_runtime::{error::HandlerError, Context};
use scryfall::api::cards_search;
use serde_json;
use telegram::messages::{MessageEntityType, ParseMode, SendMessage, TelegramUpdate};

mod convert;
mod scryfall;
mod telegram;

fn main() -> Result<(), Box<dyn Error>> {
    lambda!(my_handler);

    Ok(())
}

fn my_handler(event: Request, _context: Context) -> Result<impl IntoResponse, HandlerError> {
    let msg_body = event.into_body();
    println!("{:?}", msg_body);

    let maybe_update: Option<TelegramUpdate> = match msg_body {
        Body::Text(e) => Some(serde_json::from_str(&e).unwrap()),
        _ => None,
    };
    let update = maybe_update.expect("Unsupported content type of HTTP body.");

    if update.inline_query.is_some() {
        handle_inline_query(&update);
    }

    if update.message.is_some() {
        handle_message(&update);
    }

    Ok(Response::builder().status(200).body("").unwrap())
}

fn handle_inline_query(update: &TelegramUpdate) {
    let q = update.inline_query.as_ref().unwrap();

    if q.query.len() == 0 {
        return;
    }

    let results = cards_search(&q.query, "name", 1).unwrap();
    let response = convert::search_results_to_inline_query_response(q.id.clone(), &results);
    telegram::api::answer_inline_query(&response);
}

fn handle_message(update: &TelegramUpdate) {
    let msg = update.message.as_ref().unwrap();

    if msg.entities.is_none() {
        return;
    }

    let entities = msg.entities.as_ref().unwrap();

    if entities.len() == 0 {
        return;
    }

    let msg_text = msg.text.as_ref().unwrap();

    for cmd in entities
        .iter()
        .filter(|e| e.entity_type == MessageEntityType::BotCommand)
    {
        let command_txt: String = msg_text
            .chars()
            .into_iter()
            .skip(cmd.offset as usize)
            .take(cmd.length as usize)
            .collect();

        if &command_txt == "/start" {
            telegram::api::send_message(&SendMessage {
                chat_id: msg.chat.id.clone(),
                parse_mode: Some(ParseMode::Markdown),
                disable_web_page_preview: Some(true),
                text: "Welcome to ScryfallBot!

*Usage*
ScryfallBot is an _inline_ bot, meaning you just tag @ScryfallBot and start typing while the results show up above your keyboard.
Tapping a result will send it in your chat. All Scryfall syntax is supported, for a full overview, see [the Scryfall syntax docs](https://scryfall.com/docs/syntax)

*Questions, Improvements, Changes*
ScryfallBot is open source and lives on [Github here](https://github.com/OliverHofkens/scryfall-telegram-rs-serverless).
If you have a great idea, feature request, or bug report, feel free to [open an issue here](https://github.com/OliverHofkens/scryfall-telegram-rs-serverless/issues)

*Legal stuff*
- The code for this bot is licensed under the [MIT License](https://github.com/OliverHofkens/scryfall-telegram-rs-serverless/blob/master/LICENSE), so you're free to change it!
- I am in no way associated or affiliated with Scryfall, I just use [their fantastic, public API](https://scryfall.com/docs/api).
                ".to_string(),
            });
        } else {
            println!("Unsupported command: {}", command_txt);
        }
    }
}
