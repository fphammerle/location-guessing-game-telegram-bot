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

import unittest.mock

# pylint: disable=import-private-name; tests
from location_guessing_game_telegram_bot import _run


def test__run(tmp_path, wikimap_export_path):
    telegram_token_path = tmp_path.joinpath("token")
    telegram_token_path.write_text("secret\n")
    with unittest.mock.patch("telegram.ext.Updater") as updater_mock:
        _run(
            telegram_token_path=telegram_token_path,
            wikimap_export_path=wikimap_export_path,
        )
    updater_mock.assert_called_once()
    # > Changed in version 3.8: Added args and kwargs properties.
    # https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock.call_args_list
    init_args, init_kwargs = updater_mock.call_args
    assert not init_args
    assert set(init_kwargs.keys()) == {
        "persistence",
        "token",
        "use_context",
    }
    assert init_kwargs["token"] == "secret"
    assert init_kwargs["use_context"] is True
    photos = init_kwargs["persistence"].get_bot_data()["photos"]
    assert len(photos) == 25
    assert (
        photos[1].photo_url
        == "https://upload.wikimedia.org/wikipedia/commons/6/65/Gro%C3%9Fvenediger3.JPG"
    )
