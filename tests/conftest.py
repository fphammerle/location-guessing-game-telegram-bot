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

import json
import pathlib
import typing

import pytest

# pylint: disable=import-private-name; tests
from location_guessing_game_telegram_bot import _Photo


@pytest.fixture(scope="session")
def wikimap_export_path() -> pathlib.Path:
    return pathlib.Path(__file__).parent.joinpath(
        "resources",
        "wikimap.toolforge.org",
        "api.php@cat=Images_with_annotations&lang=de&year=2020-2020&region=48%7C12%7C47%7C13",
    )


# pylint: disable=redefined-outer-name; fixture


@pytest.fixture(scope="session")
def wikimap_export(wikimap_export_path) -> pathlib.Path:
    try:
        return json.loads(wikimap_export_path.read_text())
    except json.decoder.JSONDecodeError as exc:
        if "git-lfs.github.com" in wikimap_export_path.read_text():
            raise ValueError("git-lfs pointers unresolved") from exc
        raise


@pytest.fixture(scope="session")
def wikimap_photos(wikimap_export) -> typing.List[_Photo]:
    return [_Photo.from_wikimap_export(attrs) for attrs in wikimap_export]
