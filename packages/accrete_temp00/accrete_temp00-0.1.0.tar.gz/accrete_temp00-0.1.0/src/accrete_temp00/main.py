"""This file contains entrypoint functions for the app."""

import logging
from importlib import resources as imp_resources

import typer
from omegaconf import OmegaConf

from data_structure_and_validation import log_settings
from data_structure_and_validation.dataclass import ExampleDataset

from . import conf

CONFIG_FILENAME = imp_resources.files(conf) / "config.yaml"
LOGGING_LEVELS = set(logging._nameToLevel.keys())

app = typer.Typer()
common_args = {}
logger = logging.getLogger()


def _configure_logger(cfg, logger_settings):
    log_settings.configure_root_logger(
        cfg,
        log_level=logging.getLevelName(logger_settings["log_level"]),
        write_to_files=logger_settings["write_log_files"],
        log_dir=logger_settings["log_dir"],
    )


@app.callback()
def _log_args(
    log_level: str = typer.Option(
        "DEBUG", "--log-level", help="Sets log level"
    ),
    write_log_files: bool = typer.Option(
        False, "--write-log-files", help="If set outputs log files"
    ),
    log_dir: str = typer.Option(
        "./", "--log-dir", help="Specifies dir to write log files"
    ),
):
    common_args["log_level"] = log_level
    common_args["write_log_files"] = write_log_files
    common_args["log_dir"] = log_dir


@app.command()
def hello_world() -> None:
    """Log hello to the world."""
    cfg = OmegaConf.load(CONFIG_FILENAME)
    _configure_logger(cfg, common_args)
    logger.info("Hello, world!")


@app.command()
def create_dataset() -> None:
    """Log dataset creation."""
    cfg = OmegaConf.load(CONFIG_FILENAME)
    _configure_logger(cfg, common_args)
    logger.info(f"Created dataset object from: {cfg.dataFrame_path}...")
    data = ExampleDataset(cfg.dataFrame_path, cfg.schema_path)
    logger.info(f"Created dataset object: {type(data)}.")


if __name__ == "__main__":
    app()
