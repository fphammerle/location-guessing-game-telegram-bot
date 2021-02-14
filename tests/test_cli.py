import logging
import pathlib
import unittest.mock

import pytest

from location_guessing_game_telegram_bot import _main


@pytest.mark.parametrize(
    ("args", "env", "telegram_token_path", "wikimap_export_path"),
    (
        (
            [
                "--telegram-token-path",
                "/telegram/token.txt",
                "--wikimap-export-path",
                "/wikimap/export.json",
            ],
            {},
            "/telegram/token.txt",
            "/wikimap/export.json",
        ),
        (
            [
                "--telegram-token-path",
                "/telegram/token.txt",
                "--wikimap-export-path",
                "/wikimap/export.json",
            ],
            {
                "TELEGRAM_TOKEN_PATH": "overruled.txt",
                "WIKIMAP_EXPORT_PATH": "/ineffective.json",
            },
            "/telegram/token.txt",
            "/wikimap/export.json",
        ),
        (
            ["--wikimap-export-path", "/wikimap/export.json"],
            {
                "TELEGRAM_TOKEN_PATH": "/telegram/token-via-env.txt",
                "WIKIMAP_EXPORT_PATH": "/ineffective.json",
            },
            "/telegram/token-via-env.txt",
            "/wikimap/export.json",
        ),
        (
            [],
            {
                "TELEGRAM_TOKEN_PATH": "/telegram/token-via-env.txt",
                "WIKIMAP_EXPORT_PATH": "/export.json",
            },
            "/telegram/token-via-env.txt",
            "/export.json",
        ),
    ),
)
def test__main(args, env, telegram_token_path, wikimap_export_path):
    with unittest.mock.patch(
        "location_guessing_game_telegram_bot._run"
    ) as run_mock, unittest.mock.patch(
        "sys.argv", [""] + args
    ), unittest.mock.patch.dict(
        "os.environ", env
    ):
        _main()
    run_mock.assert_called_once_with(
        telegram_token_path=pathlib.Path(telegram_token_path),
        wikimap_export_path=pathlib.Path(wikimap_export_path),
    )


@pytest.mark.parametrize(
    ("args", "root_log_level", "log_format"),
    (
        ([], logging.INFO, "%(message)s"),
        (
            ["--debug"],
            logging.DEBUG,
            "%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s",
        ),
    ),
)
def test_logging_config(args, root_log_level, log_format):
    with unittest.mock.patch(
        "location_guessing_game_telegram_bot._run"
    ) as run_mock, unittest.mock.patch(
        "sys.argv",
        ["", "--telegram-token-path", "/t", "--wikimap-export-path", "/w"] + args,
    ), unittest.mock.patch(
        "logging.basicConfig"
    ) as logging_basic_config_mock:
        _main()
    run_mock.assert_called_once_with(
        telegram_token_path=pathlib.Path("/t"), wikimap_export_path=pathlib.Path("/w")
    )
    assert logging_basic_config_mock.call_count == 1
    assert logging_basic_config_mock.call_args[1]["level"] == root_log_level
    assert logging_basic_config_mock.call_args[1]["format"] == log_format
