# location-guessing-game-telegram-bot - Telegram Bot Sending Random Wikimedia Commons Photos
#
# Copyright (C) 2021 Fabian Peter Hammerle <fabian@hammerle.me>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import argparse
import json
import logging
import os
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
        return "photo " + self.description_url

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
    assert isinstance(context.chat_data, dict)  # mypy
    assert update.effective_chat is not None  # mypy
    if "last_photo_message_id" in context.chat_data:
        update.effective_chat.send_message(
            text="Lösung: {}".format(context.chat_data["last_photo"].description_url),
            disable_web_page_preview=True,
            reply_to_message_id=context.chat_data["last_photo_message_id"],
        )
        # https://github.com/python-telegram-bot/python-telegram-bot/pull/2043
        update.effective_chat.send_location(
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
        _LOGGER.info("sending %s", photo)
        try:
            with urllib.request.urlopen(photo.photo_url) as photo_response:
                photo_message = update.effective_chat.send_photo(
                    photo=photo_response,
                    caption="Wo wurde dieses Photo aufgenommen?",
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

    def get_user_data(self) -> typing.DefaultDict[int, dict]:
        raise NotImplementedError()  # pragma: no cover

    def get_chat_data(self) -> typing.DefaultDict[int, dict]:
        raise NotImplementedError()  # pragma: no cover

    def get_bot_data(self) -> dict:
        return self._bot_data

    def get_conversations(self, name: str) -> dict:
        return {}  # pragma: no cover

    def update_user_data(self, user_id: int, data: dict) -> None:
        pass  # pragma: no cover

    def update_chat_data(self, chat_id: int, data: dict) -> None:
        pass  # pragma: no cover

    def update_bot_data(self, data: dict) -> None:
        pass  # pragma: no cover

    def update_conversation(
        self, name: str, key: tuple, new_state: typing.Optional[object]
    ) -> None:
        pass  # pragma: no cover


# https://git.hammerle.me/fphammerle/pyftpd-sink/src/5daf383bc238425cd37d011959a8eeffab0112c3/pyftpd-sink#L48
class _EnvDefaultArgparser(argparse.ArgumentParser):
    def add_argument(self, *args, envvar=None, **kwargs):
        # pylint: disable=arguments-differ; using *args & **kwargs to catch all
        if envvar:
            envvar_value = os.environ.get(envvar, None)
            if envvar_value:
                kwargs["required"] = False
                kwargs["default"] = envvar_value
        super().add_argument(*args, **kwargs)


def _run(telegram_token_path: pathlib.Path, wikimap_export_path: pathlib.Path) -> None:
    photos = [
        _Photo.from_wikimap_export(attrs)
        for attrs in json.loads(wikimap_export_path.read_text())
    ]
    updater = telegram.ext.Updater(
        token=telegram_token_path.read_text().rstrip(),
        use_context=True,
        persistence=_Persistence(photos=photos),
    )
    updater.dispatcher.add_handler(telegram.ext.CommandHandler("photo", _photo_command))
    updater.start_polling()


def _main():
    argparser = _EnvDefaultArgparser()
    argparser.add_argument(
        "--telegram-token-path",
        type=pathlib.Path,
        required=True,
        envvar="TELEGRAM_TOKEN_PATH",
        help="default: env var TELEGRAM_TOKEN_PATH",
    )
    argparser.add_argument(
        "--wikimap-export-path",
        type=pathlib.Path,
        required=True,
        envvar="WIKIMAP_EXPORT_PATH",
        help="https://wikimap.toolforge.org/api.php?[...] json, "
        "default: env var WIKIMAP_EXPORT_PATH",
    )
    argparser.add_argument("--debug", action="store_true")
    args = argparser.parse_args()
    # https://github.com/fphammerle/python-cc1101/blob/26d8122661fc4587ecc7c73df55b92d05cf98fe8/cc1101/_cli.py#L51
    logging.basicConfig(
        level=logging.DEBUG if args.debug else logging.INFO,
        format="%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s"
        if args.debug
        else "%(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S%z",
    )
    _LOGGER.debug("args=%r", args)
    _run(
        telegram_token_path=args.telegram_token_path,
        wikimap_export_path=args.wikimap_export_path,
    )
