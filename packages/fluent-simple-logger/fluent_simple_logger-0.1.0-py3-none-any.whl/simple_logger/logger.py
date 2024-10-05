import sys
from datetime import datetime, date

class Logger:
    def __init__(self, log_file: str = f'{date.today()}_log.txt', prefix: str = '[Simple Logger]') -> None:
        """
        Initializes the Logger instance.

        Args:
            log_file (str): The name of the log file. Defaults to today's date followed by '_log.txt'.
            prefix (str): The prefix to be used in log messages. Defaults to '[Simple Logger]'.
        """
        self.PREFIX = f'\033[1;36m{prefix} \033[0m'
        self.colors = {
            'error': "\033[1;31m",
            'warning': "\033[1;33m",
            'debug': "\033[1;34m",
            'critical': "\033[1;41m",
            'reset': "\033[0m"
        }
        self.log_file = log_file

    def _log_to_file(self, message: str) -> None:
        """
        Appends a message to the log file with a timestamp.

        Args:
            message (str): The message to be logged.
        """
        with open(self.log_file, 'a') as file:
            file.write(f"{datetime.now()} - {message}\n")

    def _log(self, message: str) -> None:
        """
        Prints a message to the console.

        Args:
            message (str): The message to be printed.
        """
        print(message)

    def info(self, _message: str) -> None:
        """
        Logs an informational message both to the console and the log file.

        Args:
            _message (str): The message to log.
        """
        self._log(self.PREFIX + _message)
        self._log_to_file("INFO - " + _message)

    def error(self, _message: str) -> None:
        """
        Logs an error message both to the console and the log file.

        Args:
            _message (str): The error message to log.
        """
        log_message = self.PREFIX + self.colors['error'] + "ERROR: " + _message + self.colors['reset']
        self._log(log_message)
        self._log_to_file("ERROR - " + _message)

    def warning(self, _message: str) -> None:
        """
        Logs a warning message both to the console and the log file.

        Args:
            _message (str): The warning message to log.
        """
        log_message = self.PREFIX + self.colors['warning'] + "WARN: " + _message + self.colors['reset']
        self._log(log_message)
        self._log_to_file("WARNING - " + _message)

    def debug(self, _message: str) -> None:
        """
        Logs a debug message both to the console and the log file.

        Args:
            _message (str): The debug message to log.
        """
        log_message = self.PREFIX + self.colors['debug'] + "DEBUG: " + _message + self.colors['reset']
        self._log(log_message)
        self._log_to_file("DEBUG - " + _message)

    def critical(self, _message: str) -> None:
        """
        Logs a critical error message both to the console and the log file,
        and then exits the program.

        Args:
            _message (str): The critical message to log.
        """
        log_message = self.PREFIX + self.colors['critical'] + "CRITICAL: " + _message + self.colors['reset']
        self._log(log_message)
        self._log_to_file("CRITICAL - " + _message)
        sys.exit(1)

    def set_prefix(self, new_prefix: str) -> None:
        """
        Sets a new prefix for log messages.

        Args:
            new_prefix (str): The new prefix to set.
        """
        self.PREFIX = f'\033[1;36m{new_prefix} \033[0m'
