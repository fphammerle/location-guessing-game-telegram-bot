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

import pathlib

import setuptools

_REPO_URL = "https://github.com/fphammerle/location-guessing-game-telegram-bot"

setuptools.setup(
    name="location-guessing-game-telegram-bot",
    use_scm_version={
        # > AssertionError: cant parse version docker/0.1.0-amd64
        # https://github.com/pypa/setuptools_scm/blob/master/src/setuptools_scm/git.py#L15
        "git_describe_command": "git describe --dirty --tags --long --match v*",
    },
    packages=setuptools.find_packages(),
    description="Basic Telegram Bot Sending Random Wikimedia Commons Photos",
    long_description=pathlib.Path(__file__).parent.joinpath("README.md").read_text(),
    long_description_content_type="text/markdown",
    author="Fabian Peter Hammerle",
    author_email="fabian+location-guessing@hammerle.me",
    url=_REPO_URL,
    project_urls={"Changelog": _REPO_URL + "/blob/master/CHANGELOG.md"},
    license="GPLv3+",
    keywords=[
        "bot",
        "game",
        "guessing",
        "location",
        "photos",
        "telegram",
    ],
    classifiers=[
        # https://pypi.org/classifiers/
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Topic :: Games/Entertainment",
        # .github/workflows/python.yml
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    entry_points={
        "console_scripts": [
            "location-guessing-game-telegram-bot = location_guessing_game_telegram_bot:_main",
        ]
    },
    # >=3.6 f-strings & force kwargs with *
    # >=3.7 postponed evaluation of type annotations (PEP563) & dataclass
    python_requires=">=3.8",  # python<3.8 untested
    install_requires=[
        # >=13.0 provides telegram.chat.Chat.send_location shortcut
        # https://github.com/python-telegram-bot/python-telegram-bot/commit/fc5844c13da3b3fb20bb2d0bfcdf1efb1a826ba6#diff-2590f2bde47ea3730442f14a3a029ef77d8f2c8f3186cf5edd7e18bcc7243c39R381
        # >=13.0 requires python>=3.6
        # https://github.com/python-telegram-bot/python-telegram-bot/commit/19a4f9e53a1798b886fd4ce3e5a9a48db9ae5152#diff-60f61ab7a8d1910d86d9fda2261620314edcae5894d5aaa236b821c7256badd7L64
        # v20.0 made module `telegram.update` private
        # https://github.com/python-telegram-bot/python-telegram-bot/commit/5275c451994438b1184dd395b36fc8ae61369037#diff-361ea8462f85b6a84d97ac5b72c7d0c906c1970347033343cf0efc0bf2d13ec4
        # https://github.com/python-telegram-bot/python-telegram-bot/pull/2687
        "python-telegram-bot>=13.0,<20.0"
    ],
    setup_requires=["setuptools_scm"],
    tests_require=["pytest"],
)
