"""This file contains functions for customizing the package logger."""

import logging
import os
from logging.handlers import RotatingFileHandler

from omegaconf import DictConfig

# Formats to use when outputting a message:
DEBUG_FORMATTER_FMT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
INFO_FORMATTER_FMT = "%(asctime)s - %(levelname)s - %(message)s"

# Other settings;
FORMATTER_TIMESTAMP = "%Y-%m-%d %H:%M:%S"


def set_up_log_filehandler(
    cfg: DictConfig,
    logger: logging.Logger,
    log_level: int,
    filepath: str,
    output_format,
) -> None:
    """Set up logger filehandler to write to a file.

    Args:
        cfg: Config settings for which to set the logger.
        logger: Existing logger to set up the handler for.
        log_level: Level at which to configure filehandler.
        filepath: The filepath where the file should log messages.
        output_format: The Formatter format for messages.
    """
    fh = RotatingFileHandler(
        filepath,
        maxBytes=cfg.max_file_bytes,
        backupCount=cfg.backup_file_count,
    )
    fh.setLevel(log_level)
    formatter = logging.Formatter(output_format, FORMATTER_TIMESTAMP)
    fh.setFormatter(formatter)
    logger.addHandler(fh)


def set_up_streamhandler(
    cfg: DictConfig, logger: logging.Logger, log_level: int
) -> None:
    """Set up a logger streamhandler.

    Args:
        cfg: Config settings for which to set the logger.
        logger: Existing logger to set up the handler for.
        log_level: Level at which to configure filehandler.
    """
    sh = logging.StreamHandler()
    sh.setLevel(log_level)

    if log_level == logging.DEBUG:
        fmt = DEBUG_FORMATTER_FMT
    else:
        fmt = INFO_FORMATTER_FMT

    formatter = logging.Formatter(fmt, FORMATTER_TIMESTAMP)
    sh.setFormatter(formatter)
    logger.addHandler(sh)

    log_level_as_string = logging.getLevelName(logger.getEffectiveLevel())
    logger.debug(f"Streamhandler set at level {log_level_as_string}")


def configure_root_logger(
    cfg: DictConfig, log_level: int, write_to_files: bool, log_dir: str
) -> None:
    """Invoke functions to set up logger handlers.

    Args:
        cfg: Config settings for which to set the logger.
        log_level: Level at which to log.
        write_to_files: Whether or not to write logs to files.
        log_dir: If write_to_files is True, indicates to write to files.
            Else, causes write_to_files to be not used.
    """
    logger = logging.getLogger()

    logger.setLevel(log_level)
    set_up_streamhandler(cfg, logger, log_level)

    if write_to_files:
        os.makedirs(log_dir, exist_ok=True)

        # Assume no race conditions here in this dummy app:
        current_log_level = logger.getEffectiveLevel()

        if current_log_level <= logging.DEBUG:
            debug_filepath = os.path.join(log_dir, cfg.debug_file)
            set_up_log_filehandler(
                cfg, logger, logging.DEBUG, debug_filepath, DEBUG_FORMATTER_FMT
            )
            logger.debug(f"DEBUG logs writing to filepath {debug_filepath}")

        if current_log_level <= logging.INFO:
            info_filepath = os.path.join(log_dir, cfg.info_file)
            set_up_log_filehandler(
                cfg, logger, logging.INFO, info_filepath, INFO_FORMATTER_FMT
            )
            logger.debug(f"INFO logs writing to filepath {info_filepath}")
