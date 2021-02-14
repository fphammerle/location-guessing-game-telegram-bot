import pathlib

import setuptools

_REPO_URL = "https://github.com/fphammerle/location-guessing-game-telegram-bot"

setuptools.setup(
    name="location-guessing-game-telegram-bot",
    use_scm_version=True,
    packages=setuptools.find_packages(),
    description="Basic Telegram Bot Sending Random Wikimedia Commons Photos",
    long_description=pathlib.Path(__file__).parent.joinpath("README.md").read_text(),
    long_description_content_type="text/markdown",
    author="Fabian Peter Hammerle",
    author_email="fabian+location-guessing@hammerle.me",
    url=_REPO_URL,
    project_urls={"Changelog": _REPO_URL + "/blob/master/CHANGELOG.md"},
    keywords=["bot", "game", "guessing", "location", "photos", "telegram",],
    classifiers=[
        # https://pypi.org/classifiers/
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "Operating System :: OS Independent",
        "Topic :: Games/Entertainment",
        # .github/workflows/python.yml TODO
        # "Programming Language :: Python :: 3.5",
        # "Programming Language :: Python :: 3.6",
        # "Programming Language :: Python :: 3.7",
        # "Programming Language :: Python :: 3.8",
        # "Programming Language :: Python :: 3.9",
    ],
    entry_points={
        "console_scripts": [
            "location-guessing-game-telegram-bot = location_guessing_game_telegram_bot:_main",
        ]
    },
    install_requires=[
        # >=13.0 telegram.chat.Chat.send_location shortcut
        # https://github.com/python-telegram-bot/python-telegram-bot/commit/fc5844c13da3b3fb20bb2d0bfcdf1efb1a826ba6#diff-2590f2bde47ea3730442f14a3a029ef77d8f2c8f3186cf5edd7e18bcc7243c39R381
        "python-telegram-bot >= 13.0"
    ],
    setup_requires=["setuptools_scm"],
    # tests_require=["pytest"], TODO
)
