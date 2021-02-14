# Location Guessing Game Telegram Bot 🏞️ 🌍 📌

Basic [Telegram Bot](https://telegram.org/) Sending Random [Wikimedia Commons](https://commons.wikimedia.org) Photos

## Setup

1. Download a dataset of photos via the [WikiMap API](https://de.wikipedia.org/wiki/Benutzer:DB111/Tools#WikiMap), e.g. via:
   ```sh
   wget --restrict-file-names=windows 'https://wikimap.toolforge.org/api.php?cat=Images_with_annotations&lang=de&year=2010-2015&region=49|9|46|18'
   ```
2. Generate a bot API token by sending `/newbot` to [BotFather](https://telegram.me/botfather)
3. Install bot via `pip3 install --user --upgrade location-guessing-game-telegram-bot`
   (or use [docker](https://docker.io) / [podman](https://podman.io), see below)

## Usage

1. Launch bot: `location-guessing-game-telegram-bot --telegram-token-path file-containing-api-token --wikimap-export-path wikimap-export.json`
2. Open a chat with the bot in Telegram by searching for the bot name
   previously sent to [BotFather](https://telegram.me/botfather)
3. Send `/photo`, wait, and repeat
4. Optionally add the bot to a group chat.

## Docker / Podman 🐳

Pre-built docker images are available at https://hub.docker.com/r/fphammerle/location-guessing-game-telegram-bot/tags

```sh
$ sudo docker run --name location_guessing_game_telegram_bot \
    -v /file/containing/api-token:/telegram-token:ro -e TELEGRAM_TOKEN_PATH=/telegram-token \
    -v /wikimap/export.json:/wikimap-export.json:ro -e WIKIMAP_EXPORT_PATH=/wikimap-export.json \
    --read-only --cap-drop ALL --security-opt no-new-privileges \
    docker.io/fphammerle/location-guessing-game-telegram-bot:latest
```

Optionally, replace `sudo docker` with `podman`.

Annotation of signed tags `docker/*` contains docker image digests: https://github.com/fphammerle/location-guessing-game-telegram-bot/tags

## Trivia

Why create a Telegram bot instead of web app?

I created this mini game for my family including my grandparents who are comfortable using Telegram.
