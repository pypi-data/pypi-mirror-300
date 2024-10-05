import logging
import os
from logging.handlers import RotatingFileHandler
from typing import Optional


class Logger:
  @staticmethod
  def get_logger(
    logger_name: str, log_file: Optional[str] = None, level: int = logging.INFO
  ) -> logging.Logger:
    """
    Creates and returns a logger with the specified name and configuration.

    Args:
      logger_name (str): Name of the logger.
      log_file (Optional[str]): File where logs will be stored
        (if None, no file logging).
      level (int): Logging level (default: logging.INFO).

    Returns:
      logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)

    # Avoid adding handlers multiple times if the logger already exists
    if logger.hasHandlers():
      return logger

    # Console handler for printing to stdout
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)

    formatter = logging.Formatter(
      "%(asctime)s - %(module)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Optionally create a file handler if log_file is provided
    if log_file:
      # Ensure the directory for the log file exists
      log_dir = os.path.dirname(log_file)
      if not os.path.exists(log_dir):
        os.makedirs(log_dir)

      # Create a rotating file handler (for large log file management)
      file_handler = RotatingFileHandler(
        log_file, maxBytes=5 * 1024 * 1024, backupCount=3
      )  # 5MB per file, keep 3 backups
      file_handler.setLevel(level)
      file_handler.setFormatter(formatter)
      logger.addHandler(file_handler)

    return logger
