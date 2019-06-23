# scryfall_telegram_rs #

*Note: Spritual successor to [Scryfall_Telegram](https://github.com/OliverHofkens/Scryfall_Telegram)*

Scryfall-telegram-rs is an inline [Telegram](https://telegram.org/) bot that uses
[Scryfall](https://scryfall.com/)'s API to search Magic: The Gathering cards.

All Scryfall syntax that can be understood by the API can be used. A full reference
can be found here: [Scryfall Syntax Reference](https://scryfall.com/docs/reference).

Some examples:
- Search a card by name: `@ScryfallBot Bolas`
- Search an instant that can be played in an Esper EDH deck: `@ScryfallBot id<=esper t:instant`
- Search cards that enter the battlefield tapped: `@ScryfallBot o:"~ enters the battlefield tapped"`

## Running it yourself

This bot lives on Telegram: [t.me/ScryfallBot](t.me/ScryfallBot),
but you can easily run a copy of it yourself:

### Requirements
- Rust
- Serverless framework
- A Serverless provider (the included `serverless.yml` contains config for AWS Lambda)

### Building
- Ensure these 2 variables are in your environment:
    - TELEGRAM_BOT_TOKEN: The token given to you by the [The Botfather](https://core.telegram.org/bots#6-botfather)
    - WEBHOOK_SECRET: A secret you can choose yourself. It will be used in your webhook URL.
- Run `serverless deploy` to build and deploy.
- Run `python3 scripts/register_webhook.py {webhook_url}` to register your webhook on Telegram
- You're live!
