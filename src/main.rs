use std::error::Error;

use aws_lambda_events::event::apigw::ApiGatewayProxyRequest;
use lambda_runtime::{error::HandlerError, lambda, Context};
use scryfall::api::cards_search;
use serde_json;
use telegram::messages::TelegramUpdate;

mod convert;
mod scryfall;
mod telegram;

fn main() -> Result<(), Box<dyn Error>> {
    lambda!(my_handler);

    Ok(())
}

fn my_handler(event: ApiGatewayProxyRequest, _context: Context) -> Result<(), HandlerError> {
    let body: TelegramUpdate = serde_json::from_str(&event.body.unwrap()).unwrap();

    match body.inline_query {
        Some(q) => {
            if q.query.len() == 0 {
                return Ok(());
            }

            let results = cards_search(&q.query, "name", 1).unwrap();
            let response = convert::search_results_to_inline_query_response(q.id, &results);
            telegram::api::answer_inline_query(&response);
        }
        None => (),
    }

    Ok(())
}
