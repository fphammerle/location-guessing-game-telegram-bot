#!/usr/bin/env python3

import argparse
import io
import logging
import pathlib

import requests
import telegram.ext
import telegram.update

_LOGGER = logging.getLogger(__name__)


def _start_command(
    update: telegram.update.Update,
    context: telegram.ext.callbackcontext.CallbackContext,
):
    if "last_photo_message_id" in context.chat_data:
        # https://github.com/python-telegram-bot/python-telegram-bot/pull/2043
        context.bot.send_location(
            chat_id=update.effective_chat.id,
            latitude=48,
            longitude=16,
            reply_to_message_id=context.chat_data["last_photo_message_id"],
        )
    update.effective_chat.send_message(text=f"chat_data={context.chat_data}")
    photo_request = requests.get(
        "https://upload.wikimedia.org/wikipedia/commons/c/cf/Clematis_alpina_02.jpg"
    )
    photo_message = update.effective_chat.send_photo(
        photo=io.BytesIO(photo_request.content)
    )
    context.chat_data["last_photo_message_id"] = photo_message.message_id


def _main():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S%z",
    )
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--token-path", type=pathlib.Path, required=True)
    args = argparser.parse_args()
    _LOGGER.debug("args=%r", args)
    updater = telegram.ext.Updater(
        token=args.token_path.read_text().rstrip(), use_context=True
    )
    updater.dispatcher.add_handler(telegram.ext.CommandHandler("start", _start_command))
    updater.start_polling()


if __name__ == "__main__":
    _main()
