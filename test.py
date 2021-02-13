#!/usr/bin/env python3

import argparse
import io
import json
import logging
import pathlib
import random
import typing
import urllib.request

import telegram.ext
import telegram.update

_LOGGER = logging.getLogger(__name__)


class _Photo:
    def __init__(
        self, photo_url: str, description_url: str, latitude: float, longitude: float
    ) -> None:
        self.photo_url = photo_url
        self.description_url = description_url
        self.latitude = latitude
        self.longitude = longitude

    def __str__(self) -> str:
        return "Photo({})".format(self.description_url)

    @classmethod
    def from_wikimap_export(cls, data: dict) -> "_Photo":
        if isinstance(data["coordinates"], list):
            coords = data["coordinates"][0]
        else:
            coords = data["coordinates"]["1"]
        assert len(data["imageinfo"]) == 1, data["imageinfo"]
        return cls(
            latitude=coords["lat"],
            longitude=coords["lon"],
            photo_url=data["imageinfo"][0]["url"],
            description_url=data["imageinfo"][0]["descriptionurl"],
        )


def _photo_command(
    update: telegram.update.Update,
    context: telegram.ext.callbackcontext.CallbackContext,
):
    if "last_photo_message_id" in context.chat_data:
        update.effective_chat.send_message(
            text="Lösung: {}".format(context.chat_data["last_photo"].description_url),
            disable_web_page_preview=True,
            reply_to_message_id=context.chat_data["last_photo_message_id"],
        )
        # https://github.com/python-telegram-bot/python-telegram-bot/pull/2043
        context.bot.send_location(
            chat_id=update.effective_chat.id,
            latitude=context.chat_data["last_photo"].latitude,
            longitude=context.chat_data["last_photo"].longitude,
            disable_notification=True,
        )
        context.chat_data["last_photo_message_id"] = None
    update.effective_chat.send_message(
        text="Neues Photo wird ausgewählt und gesendet.", disable_notification=True
    )
    while True:
        photo = random.choice(context.bot_data["photos"])
        try:
            with urllib.request.urlopen(photo.photo_url) as photo_response:
                photo_message = update.effective_chat.send_photo(
                    photo=photo_response, caption="Wo wurde dieses Photo aufgenommen?",
                )
        except telegram.error.BadRequest:
            _LOGGER.warning("file size limit exceeded?", exc_info=True)
        except telegram.error.TimedOut:
            _LOGGER.warning("timeout", exc_info=True)
        else:
            break
    context.chat_data["last_photo"] = photo
    context.chat_data["last_photo_message_id"] = photo_message.message_id


class _Persistence(telegram.ext.BasePersistence):
    """
    found no easier way to inject bot_data

    https://python-telegram-bot.readthedocs.io/en/latest/telegram.ext.basepersistence.html
    """

    def __init__(self, photos: typing.List[_Photo]) -> None:
        self._bot_data = {"photos": photos}
        super().__init__(
            store_bot_data=True, store_chat_data=False, store_user_data=False
        )

    def get_user_data(self) -> dict:
        return {}

    def get_chat_data(self) -> dict:
        return {}

    def get_bot_data(self) -> dict:
        return self._bot_data

    def get_conversations(self, name: str) -> dict:
        return {}

    def update_user_data(self, user_id: int, data: dict) -> None:
        pass

    def update_chat_data(self, chat_id: int, data: dict) -> None:
        pass

    def update_bot_data(self, data: dict) -> None:
        pass

    def update_conversation(
        self, name: str, key: tuple, new_state: typing.Optional[object]
    ) -> None:
        pass


def _main():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S%z",
    )
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--token-path", type=pathlib.Path, required=True)
    argparser.add_argument(
        "--wikimap-export-path",
        type=pathlib.Path,
        required=True,
        help="https://wikimap.toolforge.org/api.php?[...] json",
    )
    args = argparser.parse_args()
    _LOGGER.debug("args=%r", args)
    photos = [
        _Photo.from_wikimap_export(attrs)
        for attrs in json.loads(args.wikimap_export_path.read_text())
    ]
    updater = telegram.ext.Updater(
        token=args.token_path.read_text().rstrip(),
        use_context=True,
        persistence=_Persistence(photos=photos),
    )
    updater.dispatcher.add_handler(telegram.ext.CommandHandler("photo", _photo_command))
    updater.start_polling()


if __name__ == "__main__":
    _main()
