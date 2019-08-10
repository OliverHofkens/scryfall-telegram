use std::error::Error;

use lambda_http::{lambda, Body, IntoResponse, Request, Response};
use lambda_runtime::{error::HandlerError, Context};
use regex::Regex;
use scryfall::api::{cards_search, single_card_image_with_fallback};
use serde_json;
use telegram::{
    inbound::{MessageEntityType, TelegramUpdate},
    outbound::{InputMediaPhoto, ParseMode, SendMediaGroup, SendMessage, SendPhoto},
};

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

    // Handle any [[ ]] references before checking for commands etc.
    handle_plaintext(update);

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
ScryfallBot works in both _inline_ mode and in active mode.
Inline mode means you just tag @ScryfallBot and start typing while the results show up above your keyboard.
Tapping a result will send it in your chat. All Scryfall syntax is supported, for a full overview, see [the Scryfall syntax docs](https://scryfall.com/docs/syntax)
Active mode means you can add ScryfallBot to a chat and look up cards by typing [[ your card here ]] in chat.

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

fn handle_plaintext(update: &TelegramUpdate) {
    let msg = &update.message.as_ref().unwrap();
    let msg_text = msg.text.to_owned();

    if msg_text.is_none() {
        return;
    }
    let msg_text = msg_text.unwrap();

    let re = Regex::new(r"\[\[(.+?)\]\]").unwrap();

    let results: Vec<String> = re
        .captures_iter(&msg_text)
        .filter_map(|cap| single_card_image_with_fallback(cap.get(1).unwrap().as_str()))
        .collect();

    if results.len() == 0 {
        return;
    }

    if results.len() == 1 {
        telegram::api::send_photo(&SendPhoto {
            chat_id: msg.chat.id.clone(),
            photo: results[0].to_owned(),
            caption: None,
            parse_mode: None,
        });
    } else {
        telegram::api::send_multi_photo(&SendMediaGroup {
            chat_id: msg.chat.id.clone(),
            media: results
                .iter()
                .map(|x| InputMediaPhoto {
                    media_type: String::from("photo"),
                    media: x.to_owned(),
                    caption: None,
                    parse_mode: None,
                })
                .collect(),
        })
    }
}
