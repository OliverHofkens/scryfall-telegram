use reqwest;
use reqwest::{RedirectPolicy, StatusCode, Url};

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
        .append_pair("include_multilingual", "true")
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

pub fn single_card_image(query: &str, set: Option<&str>) -> Option<String> {
    let base = Url::parse(BASE_URL).unwrap();
    let mut endpoint = base.join("cards/named").unwrap();

    endpoint
        .query_pairs_mut()
        .append_pair("fuzzy", query)
        .append_pair("format", "image");

    if set.is_some() {
        endpoint.query_pairs_mut().append_pair("set", set.unwrap());
    }

    let client = reqwest::Client::builder()
        .redirect(RedirectPolicy::none())
        .build()
        .unwrap();

    let response = client.get(endpoint).send().unwrap();

    match response.status() {
        StatusCode::FOUND => response
            .headers()
            .get("Location")
            .and_then(|val| Some(String::from(val.to_str().unwrap()))),
        _ => None,
    }
}

pub fn single_card_image_with_fallback(query: &str, set: Option<&str>) -> Option<String> {
    let named_result = single_card_image(query, set);

    if named_result.is_some() {
        return named_result;
    }

    let query_with_set = match set {
        Some(s) => format!("{} s:{}", query, s),
        None => String::from(query),
    };

    match cards_search(&query_with_set, "name", 1) {
        Ok(resp) => {
            for card in resp.data? {
                let images = match card.image_uris {
                    Some(_) => card.image_uris,
                    None => card.card_faces?[0].image_uris.clone(),
                };

                match images {
                    Some(img) => {
                        if img.contains_key("large") {
                            return Some(img["large"].clone());
                        }
                        continue;
                    }
                    _ => continue,
                }
            }
            None
        }
        _ => None,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_search_card_by_name() {
        let result = cards_search("Nyx-Fleece Ram", "name", 1).unwrap();

        assert_eq!(result.total_cards, Some(1));
    }

    #[test]
    fn test_get_card_by_name() {
        let result = single_card_image("Nyx-fleece ram", None);

        assert_eq!(result.is_some(), true);
    }

    #[test]
    fn test_get_card_by_name_and_set() {
        let result = single_card_image("Nyx-fleece ram", Some("JOU"));

        assert_eq!(result.is_some(), true);
    }

    #[test]
    fn test_get_card_by_name_fuzzy() {
        let result = single_card_image("bolas dragon god", None);

        assert_eq!(result.is_some(), true);
    }

    #[test]
    fn test_get_card_by_name_with_fallback_fuzzy() {
        let result = single_card_image_with_fallback("gatstaf", None);

        assert_eq!(result.is_some(), true);
    }

    #[test]
    fn test_get_card_by_name_with_fallback_fuzzy_with_set() {
        let result = single_card_image_with_fallback("gatstaf", Some("SOI"));

        assert_eq!(result.is_some(), true);
    }
}
