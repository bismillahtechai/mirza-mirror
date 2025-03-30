import logging
import os
from datetime import datetime

# Configure logging
log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
os.makedirs(log_dir, exist_ok=True)

# Create a custom logger
logger = logging.getLogger('mirza_mirror')
logger.setLevel(logging.DEBUG)

# Create handlers
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create formatters and add it to handlers
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
console_formatter = logging.Formatter(log_format)
console_handler.setFormatter(console_formatter)

# Add handlers to the logger
logger.addHandler(console_handler)

# Create a file handler that rotates daily
today = datetime.now().strftime('%Y-%m-%d')
file_handler = logging.FileHandler(os.path.join(log_dir, f'mirza_mirror_{today}.log'))
file_handler.setLevel(logging.DEBUG)
file_formatter = logging.Formatter(log_format)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

def get_logger():
    """
    Get the configured logger instance.
    
    Returns:
        Logger: Configured logger instance
    """
    return logger

def log_info(message):
    """
    Log an info message.
    
    Args:
        message: Message to log
    """
    logger.info(message)

def log_error(message, exc_info=True):
    """
    Log an error message.
    
    Args:
        message: Message to log
        exc_info: Whether to include exception info
    """
    logger.error(message, exc_info=exc_info)

def log_warning(message):
    """
    Log a warning message.
    
    Args:
        message: Message to log
    """
    logger.warning(message)

def log_debug(message):
    """
    Log a debug message.
    
    Args:
        message: Message to log
    """
    logger.debug(message)
