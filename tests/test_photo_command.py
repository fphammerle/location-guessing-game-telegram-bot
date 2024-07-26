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

import collections
import logging
import unittest.mock

import telegram.error

# pylint: disable=import-private-name; tests
from location_guessing_game_telegram_bot import _photo_command


def test_send_photo(caplog, wikimap_photos):
    update_mock = unittest.mock.MagicMock()
    update_mock.effective_chat.send_photo.return_value.message_id = "photo message id"
    context_mock = unittest.mock.MagicMock()
    context_mock.bot_data = {"photos": wikimap_photos[:1]}
    context_mock.chat_data = {}
    http_response_mock = unittest.mock.MagicMock()
    with unittest.mock.patch(
        "urllib.request.urlopen", return_value=http_response_mock
    ) as urlopen_mock, caplog.at_level(logging.INFO):
        _photo_command(update=update_mock, context=context_mock)
    assert caplog.record_tuples == [
        (
            "location_guessing_game_telegram_bot",
            logging.INFO,
            "sending photo https://commons.wikimedia.org/wiki"
            "/File:H%C3%BCtteltalkopf_(Venedigergruppe)_from_Tristkopf.jpg",
        )
    ]
    update_mock.effective_chat.send_message.assert_called_once_with(
        text="Neues Photo wird ausgewählt und gesendet.", disable_notification=True
    )
    urlopen_mock.assert_called_once_with(
        "https://upload.wikimedia.org/wikipedia/commons/a/ab"
        "/H%C3%BCtteltalkopf_%28Venedigergruppe%29_from_Tristkopf.jpg"
    )
    update_mock.effective_chat.send_photo.assert_called_once_with(
        photo=http_response_mock.__enter__(),  # pylint: disable=unnecessary-dunder-call
        caption="Wo wurde dieses Photo aufgenommen?",
    )
    assert context_mock.chat_data == {
        "last_photo": wikimap_photos[0],
        "last_photo_message_id": "photo message id",
    }


def test_send_solution_and_next_photo(caplog, wikimap_photos):
    update_mock = unittest.mock.MagicMock()
    update_mock.effective_chat.send_photo.return_value.message_id = (
        "second photo message id"
    )
    update_mock.effective_chat.id = "chat id for send_location"
    context_mock = unittest.mock.MagicMock()
    context_mock.bot_data = {"photos": wikimap_photos[1:2]}
    context_mock.chat_data = {
        "last_photo": wikimap_photos[0],
        "last_photo_message_id": "first photo message id",
    }
    http_response_mock = unittest.mock.MagicMock()
    with unittest.mock.patch(
        "urllib.request.urlopen", return_value=http_response_mock
    ) as urlopen_mock, caplog.at_level(logging.INFO):
        _photo_command(update=update_mock, context=context_mock)
    assert update_mock.effective_chat.send_message.call_count == 2
    assert update_mock.effective_chat.send_message.call_args_list[
        0
    ] == unittest.mock.call(
        text="Lösung: https://commons.wikimedia.org/wiki"
        "/File:H%C3%BCtteltalkopf_(Venedigergruppe)_from_Tristkopf.jpg",
        disable_web_page_preview=True,
        reply_to_message_id="first photo message id",
    )
    # update_mock.effective_chat.send_location.assert_called_once_with(
    context_mock.bot.send_location.assert_called_once_with(
        chat_id="chat id for send_location",
        # float comparison? :o
        latitude=47.288805,
        longitude=12.144116,
        disable_notification=True,
    )
    # next photo:
    urlopen_mock.assert_called_once_with(
        "https://upload.wikimedia.org/wikipedia/commons/6/65/Gro%C3%9Fvenediger3.JPG"
    )
    update_mock.effective_chat.send_photo.assert_called_once_with(
        photo=http_response_mock.__enter__(),  # pylint: disable=unnecessary-dunder-call
        caption="Wo wurde dieses Photo aufgenommen?",
    )
    assert context_mock.chat_data == {
        "last_photo": wikimap_photos[1],
        "last_photo_message_id": "second photo message id",
    }


def test__photo_command_file_size_exceeded(caplog, wikimap_photos):
    update_mock = unittest.mock.MagicMock()
    update_mock.effective_chat.send_photo.side_effect = [
        telegram.error.BadRequest(
            'File "/var/lib/engine/tmpfs_numa0/image.jpeg" of size 42 bytes is too big for a photo'
        )
    ] * 4 + [
        collections.namedtuple("Photo", ["message_id"])(message_id="photo message id"),
    ]
    context_mock = unittest.mock.MagicMock()
    context_mock.bot_data = {"photos": wikimap_photos[:1]}
    context_mock.chat_data = {}
    http_response_mock = unittest.mock.MagicMock()
    with unittest.mock.patch(
        "urllib.request.urlopen", return_value=http_response_mock
    ) as urlopen_mock, caplog.at_level(logging.INFO):
        _photo_command(update=update_mock, context=context_mock)
    assert urlopen_mock.call_count == 4 + 1
    assert update_mock.effective_chat.send_photo.call_count == 4 + 1
    assert len(caplog.records) == 4 * 2 + 1
    assert caplog.record_tuples[0::2] == [
        (
            "location_guessing_game_telegram_bot",
            logging.INFO,
            "sending photo https://commons.wikimedia.org/wiki"
            "/File:H%C3%BCtteltalkopf_(Venedigergruppe)_from_Tristkopf.jpg",
        )
    ] * (4 + 1)
    assert caplog.record_tuples[1::2] == [
        (
            "location_guessing_game_telegram_bot",
            logging.WARNING,
            "file size limit exceeded?",
        )
    ] * (4)
    assert context_mock.chat_data == {
        "last_photo": wikimap_photos[0],
        "last_photo_message_id": "photo message id",
    }


def test__photo_command_timeout(caplog, wikimap_photos):
    update_mock = unittest.mock.MagicMock()
    update_mock.effective_chat.send_photo.side_effect = [
        telegram.error.TimedOut
    ] * 3 + [
        collections.namedtuple("Photo", ["message_id"])(
            message_id="photo message id after timeout"
        ),
    ]
    context_mock = unittest.mock.MagicMock()
    context_mock.bot_data = {"photos": wikimap_photos[:1]}
    context_mock.chat_data = {}
    http_response_mock = unittest.mock.MagicMock()
    with unittest.mock.patch(
        "urllib.request.urlopen", return_value=http_response_mock
    ) as urlopen_mock, caplog.at_level(logging.INFO):
        _photo_command(update=update_mock, context=context_mock)
    assert urlopen_mock.call_count == 3 + 1
    assert update_mock.effective_chat.send_photo.call_count == 3 + 1
    assert len(caplog.records) == 3 * 2 + 1
    assert caplog.record_tuples[1::2] == [
        (
            "location_guessing_game_telegram_bot",
            logging.WARNING,
            "timeout",
        )
    ] * (3)
    assert context_mock.chat_data == {
        "last_photo": wikimap_photos[0],
        "last_photo_message_id": "photo message id after timeout",
    }
