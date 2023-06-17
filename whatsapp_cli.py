#!/usr/bin/env python3

import os
import logging
import argparse

import argcomplete
from heyoo import WhatsApp

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

TOKEN = os.environ["WA_TOKEN"]
PHONE_NUMBER_ID = os.environ["WA_PHONE_NUMBER_ID"]


def send_text_message(message_body, phone_number):
    messenger = WhatsApp(token=TOKEN, phone_number_id=PHONE_NUMBER_ID)
    messenger.send_message(message_body, phone_number)


def send_template_message(template_id, phone_number, template_components, lang="en_US"):
    messenger = WhatsApp(token=TOKEN, phone_number_id=PHONE_NUMBER_ID)
    messenger.send_template(
        template_id, phone_number, components=template_components, lang=lang
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="WhatsApp command line interface")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    send_text_parser = subparsers.add_parser(
        "send_text_message", help="Send a text message"
    )
    send_text_parser.add_argument("message_body", help="Message body")
    send_text_parser.add_argument("phone_number", help="Phone number")

    send_template_parser = subparsers.add_parser(
        "send_template_message", help="Send a template message"
    )
    send_template_parser.add_argument("template_id", help="Template ID")
    send_template_parser.add_argument("phone_number", help="Phone number")
    send_template_parser.add_argument(
        "-c",
        "--components",
        metavar="key=value",
        nargs="+",
        help="Template components as key-value pairs",
    )
    send_template_parser.add_argument(
        "-l",
        "--lang",
        default="en_US",
        help="Language for the template (optional)",
    )

    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    if args.command == "send_text_message":
        send_text_message(args.message_body, args.phone_number)
    elif args.command == "send_template_message":
        if args.components:
            components = dict(component.split("=") for component in args.components)
        else:
            components = []
        send_template_message(
            args.template_id,
            args.phone_number,
            components,
            lang=args.lang,
        )
    else:
        print(
            "Invalid command. Available commands: send_text_message, send_template_message"
        )
