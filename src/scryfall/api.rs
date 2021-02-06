use reqwest;
use reqwest::{StatusCode, Url};
use strsim::levenshtein;

use crate::scryfall::models::{Card, Face, SearchResult};
use std::collections::HashMap;

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

pub fn single_card_image(query: &str, set: Option<&str>) -> reqwest::Result<Option<String>> {
    let base = Url::parse(BASE_URL).unwrap();
    let mut endpoint = base.join("cards/named").unwrap();

    endpoint.query_pairs_mut().append_pair("fuzzy", query);

    if set.is_some() {
        endpoint.query_pairs_mut().append_pair("set", set.unwrap());
    }

    let response = reqwest::get(endpoint)?.error_for_status();

    match response {
        Ok(mut resp) => {
            let res: Card = resp.json().unwrap();
            Ok(image_for_card(&res, query, "normal"))
        }
        Err(e) => Err(e),
    }
}

pub fn single_card_image_with_fallback(
    query: &str,
    set: Option<&str>,
) -> reqwest::Result<Option<String>> {
    let named_result = single_card_image(query, set).ok().flatten();

    if named_result.is_some() {
        return Ok(named_result);
    }

    let query_with_set = match set {
        Some(s) => format!("{} s:{}", query, s),
        None => String::from(query),
    };

    let search_res = cards_search(&query_with_set, "name", 1)?;
    match search_res.data {
        Some(cards) => Ok(cards
            .first()
            .and_then(|c| image_for_card(c, query, "normal"))),
        None => Ok(None),
    }
}

fn _image_for_face_with_name<'a>(
    faces: &'a Vec<Face>,
    name: &str,
) -> Option<&'a HashMap<String, String>> {
    let wanted_face = faces.iter().min_by_key(|f| levenshtein(&f.name, name))?;
    wanted_face.image_uris.as_ref()
}

fn image_for_card(card: &Card, name_of_interest: &str, preferred_format: &str) -> Option<String> {
    // NOTE: Split cards, adventures, etc. have multiple `card_faces`, but the
    // image only exists on the root level. Meanwhile, double faced cards have
    // images per `card_face`. We _could_ check on the `layout` field, but for
    // now it seems sensible to just check where `image_uris` is found.
    let face_images = card
        .card_faces
        .as_ref()
        .and_then(|f| _image_for_face_with_name(f, name_of_interest));

    let images = &card.image_uris.as_ref().or(face_images)?;

    images
        .get(preferred_format)
        .cloned()
        .or_else(|| images.values().next().cloned())
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
        let result = single_card_image("Nyx-fleece ram", None).unwrap();

        assert_eq!(result.is_some(), true);
    }

    #[test]
    fn test_get_card_by_name_and_set() {
        let result = single_card_image("Nyx-fleece ram", Some("JOU")).unwrap();

        assert_eq!(result.is_some(), true);
    }

    #[test]
    fn test_get_card_by_name_fuzzy() {
        let result = single_card_image("bolas dragon god", None).unwrap();

        assert_eq!(result.is_some(), true);
    }

    #[test]
    fn test_get_double_faced_card_by_name() {
        let result_front = single_card_image("Delver of Secrets", None).unwrap();
        let result_back = single_card_image("Insectile Aberration", None).unwrap();

        assert_eq!(result_front.is_some(), true);
        assert_eq!(result_back.is_some(), true);
        assert_ne!(result_front.unwrap(), result_back.unwrap())
    }

    #[test]
    fn test_get_split_adventure_card_by_name() {
        let result_adv = single_card_image("Stomp", None).unwrap();
        let result_creature = single_card_image("Bonecrusher Giant", None).unwrap();

        assert_eq!(result_adv.is_some(), true);
        assert_eq!(result_creature.is_some(), true);
        assert_eq!(result_adv.unwrap(), result_creature.unwrap())
    }

    #[test]
    fn test_get_split_card_by_name() {
        let result_top = single_card_image("Commit", None).unwrap();
        let result_bottom = single_card_image("Memory", None).unwrap();
        let result_both = single_card_image("Commit // Memory", None).unwrap();

        assert_eq!(result_top.is_some(), true);
        assert_eq!(result_bottom.is_some(), true);
        assert_eq!(result_both.is_some(), true);
        assert_eq!(result_top.unwrap(), result_bottom.unwrap())
    }

    #[test]
    fn test_get_card_by_name_with_fallback_fuzzy() {
        let result = single_card_image_with_fallback("nyx", None).unwrap();

        assert_eq!(result.is_some(), true);
    }

    #[test]
    fn test_get_double_faced_card_by_name_with_fallback_fuzzy() {
        let result = single_card_image_with_fallback("gatstaf", None).unwrap();

        assert_eq!(result.is_some(), true);
    }

    #[test]
    fn test_get_card_by_name_with_fallback_fuzzy_with_set() {
        let result = single_card_image_with_fallback("gatstaf", Some("SOI")).unwrap();

        assert_eq!(result.is_some(), true);
    }
}
