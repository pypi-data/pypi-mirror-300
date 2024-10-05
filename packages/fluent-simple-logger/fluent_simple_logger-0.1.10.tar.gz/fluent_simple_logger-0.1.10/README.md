# Simple Logger

Simple Logger is a simple and customizable logging library for Python. It provides various logging levels with colored output for better visibility in the console and logs messages to a specified file.

## Features

- **Multiple Log Levels**: Log messages with different severity levels, including INFO, WARNING, ERROR, DEBUG, and CRITICAL.
- **Custom Prefix**: Easily customize the prefix for all log messages.
- **Colored Output**: Get colorful console output for better readability.
- **File Logging**: Automatically logs messages to a file with a timestamp.
- **Graceful Error Handling**: Stops execution on critical errors with a clear message.

## Installation

You can install the library using pip:

```bash
pip install fluent-simple-logger
```

## Usage

Here's a quick example of how to use Simple Logger:

```python
from simple_logger.logger import Logger

# Create a logger instance
logger = Logger()

# Log messages
logger.info("This is an informational message.")
logger.warning("This is a warning message.")
logger.error("This is an error message.")
logger.debug("This is a debug message.")
logger.critical("This is a critical error message.")
```

### Custom Prefix

You can customize the prefix used in log messages like this:

```python
logger.set_prefix("[Custom Prefix]")
logger.info("This is an info message with a custom prefix.")
```

### Logging to a Specific File
You can specify a different log file when creating the logger instance:

```python 
logger = Logger(log_file='custom_log.txt')
logger.info("This message will be logged to custom_log.txt.")
```

### Running Tests
To run the tests for the Simple Logger library, you can use the following command:
```bash
python -m unittest discover tests
```

### Contributing
Contributions are welcome! If you have suggestions for improvements or want to report a bug, please create an issue or submit a pull request.

### License 
This project is licensed under the MIT License.
