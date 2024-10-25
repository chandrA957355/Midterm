import pytest
import logging
from decimal import Decimal
from unittest import mock
from app.calculation import Calculation
from app.calculations import Calculations
from main import (
    load_environment_variables,
    load_plugins,
    perform_calculation_and_display,
    run_repl,
    main
)

# Mock the logging configuration
@pytest.fixture(autouse=True)
def mock_configure_logging():
    with mock.patch('logger_config.configure_logging'):
        yield

# Test environment variables loading
def test_load_environment_variables():
    with mock.patch('os.environ', {"LOG_LEVEL": "DEBUG"}):
        settings = load_environment_variables()
        assert settings["LOG_LEVEL"] == "DEBUG"

# Test loading plugins
def test_load_plugins():
    with mock.patch('os.path.exists', return_value=True), \
         mock.patch('os.listdir', return_value=['add_command.py']), \
         mock.patch('importlib.import_module', return_value=mock.Mock()):
        commands = load_plugins()
        assert "add" in commands

# Test loading plugins with missing directory
def test_load_plugins_missing_directory():
    with mock.patch('os.path.exists', return_value=False):
        commands = load_plugins()
        assert len(commands) == 0

# Test perform_calculation_and_display with invalid command
def test_perform_calculation_and_display_invalid_command():
    commands = {}
    with mock.patch("builtins.print") as mock_print:
        perform_calculation_and_display("2", "3", "unknown", commands)
        mock_print.assert_called_once_with("Unknown operation: unknown")

# Test perform_calculation_and_display with multiprocessing
def test_perform_calculation_and_display_multiprocessing():
    commands = {
        "add": mock.Mock()
    }
    commands["add"].execute_multiprocessing = mock.Mock()

    with mock.patch("builtins.print"), mock.patch("multiprocessing.Queue"), \
         mock.patch("multiprocessing.Process") as mock_process:
        perform_calculation_and_display("2", "3", "add", commands, use_multiprocessing=True)
        mock_process.assert_called_once()

# Test REPL run
def test_run_repl():
    commands = {
        "add": mock.Mock()
    }
    with mock.patch("builtins.input", side_effect=["menu", "exit"]), \
         mock.patch("builtins.print"):
        run_repl(commands)

# Test main function with arguments
def test_main_with_arguments():
    with mock.patch("sys.argv", ["main.py", "2", "3", "add"]), \
         mock.patch("main.perform_calculation_and_display") as mock_perform:
        main()
        mock_perform.assert_called_once()

# Test main function with REPL
def test_main_with_repl():
    with mock.patch("sys.argv", ["main.py", "repl"]), \
         mock.patch("main.run_repl") as mock_repl:
        main()
        mock_repl.assert_called_once()

# Test main function with no arguments
def test_main_no_arguments():
    with mock.patch("sys.argv", ["main.py"]), \
         mock.patch("builtins.print") as mock_print:
        main()
        mock_print.assert_called_once_with("Usage: python main.py <number1> <number2> <operation> [mp] or python main.py repl")
