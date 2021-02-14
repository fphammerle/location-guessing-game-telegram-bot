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

import pytest

from location_guessing_game_telegram_bot import _Photo


@pytest.mark.parametrize(
    ("index", "expected_vars"),
    (
        (
            0,
            {
                "description_url": "https://commons.wikimedia.org/wiki"
                "/File:H%C3%BCtteltalkopf_(Venedigergruppe)_from_Tristkopf.jpg",
                "latitude": 47.288805,
                "longitude": 12.144116,
                "photo_url": "https://upload.wikimedia.org/wikipedia/commons/a/ab"
                "/H%C3%BCtteltalkopf_%28Venedigergruppe%29_from_Tristkopf.jpg",
            },
        ),
        (
            1,
            {
                "description_url": "https://commons.wikimedia.org/wiki"
                "/File:Gro%C3%9Fvenediger3.JPG",
                "latitude": 47.24854167,
                "longitude": 12.25381667,
                "photo_url": "https://upload.wikimedia.org/wikipedia/commons/6/65"
                "/Gro%C3%9Fvenediger3.JPG",
            },
        ),
        # coordinates["1"]
        (
            8,
            {
                "description_url": "https://commons.wikimedia.org/wiki"
                "/File:Kasern_-_hinteres_Ahrntal.JPG",
                "latitude": 47.06111,
                "longitude": 12.15333,
                "photo_url": "https://upload.wikimedia.org/wikipedia/commons/c/ce"
                "/Kasern_-_hinteres_Ahrntal.JPG",
            },
        ),
    ),
)
def test_from_wikimap_export(wikimap_export, index, expected_vars):
    # https://github.com/pytest-dev/pytest/issues/3164 recursive pytest.approx not available
    assert vars(_Photo.from_wikimap_export(wikimap_export[index])) == expected_vars


def test___str__():
    assert (
        str(
            _Photo(
                photo_url="https://upload.wikimedia.org/wikipedia/commons/6/65"
                "/Gro%C3%9Fvenediger3.JPG",
                description_url="https://commons.wikimedia.org/wiki"
                "/File:Gro%C3%9Fvenediger3.JPG",
                latitude=47.24854167,
                longitude=12.25381667,
            )
        )
        == "photo https://commons.wikimedia.org/wiki/File:Gro%C3%9Fvenediger3.JPG"
    )
