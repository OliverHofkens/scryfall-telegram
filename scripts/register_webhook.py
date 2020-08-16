#!/usr/bin/env python3

import argparse
import os

import requests

STAGES = {"staging": "STAG", "production": "PROD"}


def main():
    parser = argparse.ArgumentParser(description="Register a webhook for your bot")
    parser.add_argument("stage", help="The stage to register the webhook for")
    parser.add_argument("url", help="The URL to register as webhook")
    args = parser.parse_args()

    try:
        stage_code = STAGES[args.stage]
    except KeyError:
        raise ValueError(f"Unknown stage {args.stage}")

    try:
        bot_token = os.environ[f"TELEGRAM_BOT_TOKEN_{stage_code}"]
    except KeyError:
        raise ValueError(
            f"Could not find TELEGRAM_BOT_TOKEN_{stage_code} in environment"
        )

    resp = requests.post(
        f"https://api.telegram.org/bot{bot_token}/setWebhook", json={"url": args.url}
    )
    resp.raise_for_status()
    print(f"[OK] Registered webhook: {args.url}")


if __name__ == "__main__":
    main()
