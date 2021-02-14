# Location Guessing Game Telegram Bot 🏞️ 🌍 📌

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![CI Pipeline Status](https://github.com/fphammerle/location-guessing-game-telegram-bot/workflows/tests/badge.svg)](https://github.com/fphammerle/location-guessing-game-telegram-bot/actions)
[![Coverage Status](https://coveralls.io/repos/github/fphammerle/location-guessing-game-telegram-bot/badge.svg?branch=master)](https://coveralls.io/github/fphammerle/location-guessing-game-telegram-bot?branch=master)
[![Last Release](https://img.shields.io/pypi/v/location-guessing-game-telegram-bot.svg)](https://pypi.org/project/location-guessing-game-telegram-bot/#history)
[![Compatible Python Versions](https://img.shields.io/pypi/pyversions/location-guessing-game-telegram-bot.svg)](https://pypi.org/project/location-guessing-game-telegram-bot/)

Basic [Telegram Bot](https://telegram.org/) Sending Random [Wikimedia Commons](https://commons.wikimedia.org) Photos

<img src="https://media.githubusercontent.com/media/fphammerle/location-guessing-game-telegram-bot/master/docs/screenshots/20210214T152031.jpg" width="40%" />&nbsp;<img src="https://media.githubusercontent.com/media/fphammerle/location-guessing-game-telegram-bot/master/docs/screenshots/20210214T152218.jpg" width="40%" />

## Setup

1. Download a dataset of photos via the [WikiMap API](https://de.wikipedia.org/wiki/Benutzer:DB111/Tools#WikiMap), for instance:
   ```sh
   wget --restrict-file-names=windows 'https://wikimap.toolforge.org/api.php?cat=Images_with_annotations&lang=de&year=2010-2015&region=49|9|46|18'
   ```
2. Generate a bot API token by sending `/newbot` to [BotFather](https://telegram.me/botfather)
3. Install bot via `pip3 install --user --upgrade location-guessing-game-telegram-bot`
   (or use [docker](https://docker.io) / [podman](https://podman.io), see below)

## Usage

1. Launch bot: `location-guessing-game-telegram-bot --telegram-token-path file-containing-api-token --wikimap-export-path wikimap-export.json`
2. Open a chat with the bot in Telegram by searching for the bot's name
   previously sent to [BotFather](https://telegram.me/botfather)
3. Send message `/photo`, wait, and repeat
4. Optionally add the bot to a group chat.

## Docker / Podman 🐳

Pre-built docker images are available at https://hub.docker.com/r/fphammerle/location-guessing-game-telegram-bot/tags

```sh
$ sudo docker run --name location_guessing_game_telegram_bot \
    -v /file/containing/api-token:/telegram-token:ro -e TELEGRAM_TOKEN_PATH=/telegram-token \
    -v /wikimap/export.json:/wikimap-export.json:ro -e WIKIMAP_EXPORT_PATH=/wikimap-export.json \
    --read-only --cap-drop ALL --security-opt no-new-privileges \
    --cpus 0.4 --memory 128M \
    docker.io/fphammerle/location-guessing-game-telegram-bot:latest
```

Optionally, replace `sudo docker` with `podman`.

Annotation of signed git tags `docker/*` contains docker image digests: https://github.com/fphammerle/location-guessing-game-telegram-bot/tags

Detached signatures of images are available at https://github.com/fphammerle/container-image-sigstore
(exluding automatically built `latest` tag).

### Docker Compose 🐙

1. Clone this repository.
2. Edit paths in `docker-compose.yml`.
3. `sudo docker-compose up --build`

### Ansible

See [ansible-playbook-example.yml](https://github.com/fphammerle/location-guessing-game-telegram-bot/blob/master/ansible-playbook-example.yml).

## Trivia

Why create a Telegram bot instead of a web app?

I created this mini game for my family including my grandparents, who are comfortable using Telegram.
