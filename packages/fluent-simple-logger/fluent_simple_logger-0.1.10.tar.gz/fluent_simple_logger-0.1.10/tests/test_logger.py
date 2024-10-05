import unittest
from simple_logger.logger import Logger
import os


class TestLogger(unittest.TestCase):

    def setUp(self):
        """Set up a temporary log file for testing."""
        self.logger = Logger(log_file='test_log.txt')

    def tearDown(self):
        """Clean up the log file after tests."""
        if os.path.exists('test_log.txt'):
            os.remove('test_log.txt')

    def test_info_logging(self):
        """Test logging an info message."""
        self.logger.info("This is an info message.")
        with open('test_log.txt', 'r') as file:
            content = file.read()
            self.assertIn("INFO - This is an info message.", content)

    def test_error_logging(self):
        """Test logging an error message."""
        self.logger.error("This is an error message.")
        with open('test_log.txt', 'r') as file:
            content = file.read()
            self.assertIn("ERROR - This is an error message.", content)

    def test_warning_logging(self):
        """Test logging a warning message."""
        self.logger.warning("This is a warning message.")
        with open('test_log.txt', 'r') as file:
            content = file.read()
            self.assertIn("WARNING - This is a warning message.", content)

    def test_debug_logging(self):
        """Test logging a debug message."""
        self.logger.debug("This is a debug message.")
        with open('test_log.txt', 'r') as file:
            content = file.read()
            self.assertIn("DEBUG - This is a debug message.", content)

    def test_critical_logging(self):
        """Test logging a critical message and ensure it exits."""
        with self.assertRaises(SystemExit):
            self.logger.critical("This is a critical message.")


if __name__ == '__main__':
    unittest.main()
