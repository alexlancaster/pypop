import io
import logging
import sys
from pathlib import Path

import pytest

from PyPop import pypop, setup_logger
from PyPop.command_line_interface import get_pypop_cli


@pytest.mark.parametrize(
    ("argv", "expected_level", "expected_file"),
    [
        (["pypop", "dummy.pop"], logging.INFO, None),  # default
        (["pypop", "-d", "dummy.pop"], logging.DEBUG, None),  # debug flag
        (
            ["pypop", "--log-level", "WARNING", "dummy.pop"],
            logging.WARNING,
            None,
        ),  # custom level
        (
            ["pypop", "--log-level", "ERROR", "dummy.pop"],
            logging.ERROR,
            None,
        ),  # error level
        (
            ["pypop", "--log-level", "CRITICAL", "dummy.pop"],
            logging.CRITICAL,
            None,
        ),  # critical level
        (
            ["pypop", "--log-file", "dummy.log", "dummy.pop"],
            logging.INFO,
            "dummy.log",
        ),  # file output
        (
            ["pypop", "-d", "--log-file", "dummy.log", "dummy.pop"],
            logging.DEBUG,
            "dummy.log",
        ),  # debug + file
    ],
)
def test_cli_logger_combinations(
    monkeypatch, tmp_path, argv, expected_level, expected_file
):
    # adjust dummy log file path
    argv = [str(tmp_path / "dummy.log") if arg == "dummy.log" else arg for arg in argv]
    if expected_file == "dummy.log":
        expected_file = str(tmp_path / "dummy.log")

    monkeypatch.setattr(sys, "argv", argv)

    # simulated main simulates what the real main() does without running analysis
    def simulated_main():
        parser = get_pypop_cli()
        args = parser.parse_args(sys.argv[1:])
        if getattr(args, "log_level", None):
            level = getattr(logging, args.log_level.upper())
        elif getattr(args, "debug", False):
            level = logging.DEBUG
        else:
            level = logging.INFO
        setup_logger(
            level=level, filename=getattr(args, "log_file", None), doctest_mode=False
        )
        return 0

    # call patched main
    monkeypatch.setattr(pypop, "main", simulated_main)
    pypop.main()

    # get the pypop logger and connect a stringio to it
    logger = logging.getLogger("pypop")
    log_stream = io.StringIO()
    stream_handler = logging.StreamHandler(log_stream)
    logger.addHandler(stream_handler)
    logger.propagate = False

    # emit test messages
    logger.debug("debug")
    logger.info("info 1")
    logger.warning("warn")
    logger.error("error")
    logger.critical("crit")
    logger.info("info 2")
    output = log_stream.getvalue()

    # Check messages according to expected level
    assert ("debug" in output) == (expected_level <= logging.DEBUG)
    assert ("info" in output) == (expected_level <= logging.INFO)
    assert ("warn" in output) == (expected_level <= logging.WARNING)
    assert ("error" in output) == (expected_level <= logging.ERROR)
    assert "crit" in output

    # if a log file was specified, check that it exists and contains messages
    if expected_file:
        file_path = Path(expected_file)
        assert file_path.exists(), f"Expected log file {file_path} not found"
        content = file_path.read_text()
        # At least one of the messages should appear in the file
        assert any(
            msg in content for msg in ["debug", "info", "warn", "error", "crit"]
        ), f"No log messages found in {file_path}"

    # close all handlers to avoid PytestUnraisableExceptionWarning
    for h in logging.getLogger("pypop").handlers[:]:
        h.close()
        logging.getLogger("pypop").removeHandler(h)
