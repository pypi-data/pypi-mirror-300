from .logging_pomes import (
    DEBUG, INFO, WARNING, ERROR, CRITICAL, PYPOMES_LOGGER,
    LOGGING_LEVEL, LOGGING_FORMAT, LOGGING_DATETIME,
    LOGGING_STYLE, LOGGING_FILEPATH, LOGGING_FILEMODE,
    logging_startup, logging_shutdown, logging_service,
    logging_get_entries, logging_send_entries
)

__all__ = [
    # logging_pomes
    "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL", "PYPOMES_LOGGER",
    "LOGGING_LEVEL", "LOGGING_FORMAT", "LOGGING_DATETIME",
    "LOGGING_STYLE", "LOGGING_FILEPATH", "LOGGING_FILEMODE",
    "logging_startup", "logging_shutdown", "logging_service",
    "logging_get_entries", "logging_send_entries"
]

from importlib.metadata import version
__version__ = version("pypomes_logging")
__version_info__ = tuple(int(i) for i in __version__.split(".") if i.isdigit())
