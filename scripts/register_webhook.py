#!/usr/bin/env python3

import argparse
import os

import requests


def main():
    parser = argparse.ArgumentParser(description="Register a webhook for your bot")
    parser.add_argument("url", help="The URL to register as webhook")
    args = parser.parse_args()

    try:
        bot_token = os.environ["TELEGRAM_BOT_TOKEN"]
    except KeyError:
        raise ValueError("Could not find TELEGRAM_BOT_TOKEN in environment")

    resp = requests.post(f"https://api.telegram.org/bot{bot_token}/setWebhook", json={
        "url": args.url
    })
    resp.raise_for_status()
    print(f"[OK] Registered webhook: {args.url}")



if __name__ == "__main__":
    main()
