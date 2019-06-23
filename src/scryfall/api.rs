use reqwest;
use reqwest::StatusCode;
use reqwest::Url;

use crate::scryfall::models::SearchResult;

const BASE_URL: &str = "https://api.scryfall.com/";

/// Returns the search result of 'query' in pages of 175 cards.
pub fn cards_search(query: &str, order: &str, page: i32) -> reqwest::Result<SearchResult> {
    let base = Url::parse(BASE_URL).unwrap();
    let mut endpoint = base.join("cards/search").unwrap();
    endpoint
        .query_pairs_mut()
        .append_pair("q", query)
        .append_pair("order", order)
        .append_pair("page", &page.to_string());

    let response = reqwest::get(endpoint)?.error_for_status();

    match response {
        Ok(mut resp) => Ok(resp.json().unwrap()),
        Err(e) => match e.status().unwrap() {
            StatusCode::NOT_FOUND => Ok(SearchResult {
                total_cards: Some(0),
                has_more: Some(false),
                data: Some(Vec::new()),
            }),
            _ => Err(e),
        },
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_get_card_by_name() {
        let result = cards_search("Nyx-Fleece Ram", "name", 1).unwrap();

        assert_eq!(result.total_cards, Some(1));
    }
}
