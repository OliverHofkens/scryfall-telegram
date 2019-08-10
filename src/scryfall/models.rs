use serde::Deserialize;
use std::collections::HashMap;

/// Some less important fields are omitted
#[derive(Deserialize)]
pub struct SearchResult {
    pub total_cards: Option<i32>,
    pub has_more: Option<bool>,
    pub data: Option<Vec<Card>>,
}

/// Unused fields are omitted
#[derive(Deserialize)]
pub struct Card {
    pub id: String,
    pub name: String,
    pub type_line: String,
    pub oracle_text: Option<String>,
    pub scryfall_uri: String,
    pub image_uris: Option<HashMap<String, String>>,
    pub card_faces: Option<Vec<Face>>,
}

/// Unused fields are omitted
#[derive(Deserialize)]
pub struct Face {
    pub image_uris: Option<HashMap<String, String>>,
}
