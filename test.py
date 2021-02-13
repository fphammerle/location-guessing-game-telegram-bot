#!/usr/bin/env python3

import argparse
import logging
import pathlib

import telegram.ext
import telegram.update

_LOGGER = logging.getLogger(__name__)


def _start_command(
    update: telegram.update.Update,
    context: telegram.ext.callbackcontext.CallbackContext,
):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"context={vars(context)}\nupdate={vars(update)}",
    )


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
