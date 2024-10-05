import contextlib
import json
import logging
from datetime import datetime, timedelta
from flask import Response, request, send_file
from logging import NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL  # 0, 10, 20, 30, 40, 50
from io import BytesIO
from pathlib import Path
from pypomes_core import (
    APP_PREFIX, DATETIME_FORMAT_INV, TEMP_FOLDER,
    env_get_str, datetime_parse, str_positional
)
from typing import Any, Final, Literal, TextIO

__LOGGING_ID: Final[str] = APP_PREFIX or "_L"
__LOGGING_DEFAULT_FORMAT: Final[str] = ("{asctime} {levelname:1.1} {thread:5d} "
                                        "{module:20.20} {funcName:20.20} {lineno:3d} {message}")
LOGGING_LEVEL: int | None = None
LOGGING_FORMAT: str | None = None
LOGGING_STYLE: str | None = None
LOGGING_DATETIME: str | None = None
LOGGING_FILEMODE: str | None = None
LOGGING_FILEPATH: Path | None = None
PYPOMES_LOGGER: logging.Logger | None = None


def logging_startup(scheme: dict[str, Any] = None) -> None:
    """
    Configure/reconfigure and start/restart the log service.

    The parameters for configuring the log can be found either as environment variables, or as
    attributes in *scheme*. Default values are used, if necessary.

    :param scheme: optional log parameters and corresponding values
    """
    scheme = scheme or {}
    global LOGGING_LEVEL, LOGGING_FORMAT, LOGGING_STYLE, \
           LOGGING_DATETIME, LOGGING_FILEMODE, LOGGING_FILEPATH, PYPOMES_LOGGER

    # noinspection PyTypeChecker
    logging_level: int = __get_logging_level(level=scheme.get("log-level",
                                                              LOGGING_LEVEL or
                                                              env_get_str(key=f"{APP_PREFIX}_LOGGING_LEVEL",
                                                                          def_value="debug").lower()))
    logging_format: str = scheme.get("log-format",
                                     LOGGING_FORMAT or
                                     env_get_str(key=f"{APP_PREFIX}_LOGGING_FORMAT",
                                                 def_value=__LOGGING_DEFAULT_FORMAT))
    logging_style: str = scheme.get("log-style",
                                    LOGGING_STYLE or
                                    env_get_str(key=f"{APP_PREFIX}_LOGGING_STYLE",
                                                def_value="{"))
    logging_datetime: str = scheme.get("log-datetime",
                                       LOGGING_DATETIME or
                                       env_get_str(key=f"{APP_PREFIX}_LOGGING_DATETIME_FORMAT",
                                                   def_value=DATETIME_FORMAT_INV))
    logging_filemode: str = scheme.get("log-filemode",
                                       LOGGING_FILEMODE or
                                       env_get_str(key=f"{APP_PREFIX}_LOGGING_FILEMODE",
                                                   def_value="w"))
    logging_filepath: Path = Path(scheme.get("log-filepath",
                                             LOGGING_FILEPATH or
                                             env_get_str(key=f"{APP_PREFIX}_LOGGING_FILEPATH",
                                                         def_value=f"{TEMP_FOLDER}/{APP_PREFIX.lower()}.log")))
    logging_filepath.parent.mkdir(parents=True,
                                  exist_ok=True)
    LOGGING_LEVEL = logging_level
    LOGGING_FORMAT = logging_format
    LOGGING_STYLE = logging_style
    LOGGING_DATETIME = logging_datetime
    LOGGING_FILEMODE = logging_filemode
    LOGGING_FILEPATH = logging_filepath

    # is there a logger ?
    if PYPOMES_LOGGER:
        # yes, shut it down
        logging.shutdown()
        force_reset: bool = True
    else:
        # no
        force_reset: bool = False

    # start and configure the logger
    PYPOMES_LOGGER = logging.getLogger(name=__LOGGING_ID)
    # noinspection PyTypeChecker
    logging.basicConfig(filename=LOGGING_FILEPATH,
                        filemode=LOGGING_FILEMODE,
                        format=LOGGING_FORMAT,
                        datefmt=LOGGING_DATETIME,
                        style=LOGGING_STYLE,
                        level=LOGGING_LEVEL,
                        force=force_reset)
    for handler in logging.root.handlers:
        handler.addFilter(filter=logging.Filter(__LOGGING_ID))


def logging_shutdown() -> None:
    """
    Invoke this function at shutdown.
    """
    global PYPOMES_LOGGER
    if PYPOMES_LOGGER:
        logging.shutdown()
        PYPOMES_LOGGER = None


def logging_get_entries(errors: list[str],
                        log_level: int = None,
                        log_from: datetime = None,
                        log_to: datetime = None) -> BytesIO:
    """
    Extract and return entries in the current logging file.

    Parameters specify criteria for log entry selection, and are optional.
    Intervals are inclusive (*[log_from, log_to]*).
    It is required that the current logging file be compliant with
    *PYPOMES_LOGGER*'s *__LOGGING_DEFAULT_STYLE*,
    or that criteria for log entry selection not be specified.

    :param errors: incidental error messages
    :param log_level: the logging level (defaults to all levels)
    :param log_from: the initial timestamp (defaults to unspecified)
    :param log_to: the finaL timestamp (defaults to unspecified)
    :return: the logging entries meeting the specified criteria
    """
    # initialize the return variable
    result: BytesIO | None = None

    # verify whether inspecting the log entries is possible
    if LOGGING_FORMAT != __LOGGING_DEFAULT_FORMAT and \
       (log_level or log_from or log_to):
        # no, report the problem
        errors.append("It is not possible to apply level "
                      "or timestamp criteria to filter log entries, "
                      "as the log format has been customized")
    else:
        # yes, proceed
        result = BytesIO()
        filepath: Path = Path(LOGGING_FILEPATH)
        with (filepath.open() as f):
            line: str = f.readline()
            while line:
                items: list[str] = line.split(sep=None,
                                              maxsplit=3)
                # noinspection PyTypeChecker
                msg_level: int = CRITICAL if not log_level or len(items) < 2 \
                                 else __get_logging_level(level=items[2].lower())
                # 'not log_level' works for both values 'NOTSET' and 'None'
                if not log_level or msg_level >= log_level:
                    if len(items) > 1 and (log_from or log_to):
                        timestamp: datetime = datetime_parse(f"{items[0]} {items[1]}")
                        if not timestamp or \
                           ((not log_from or timestamp >= log_from) and
                            (not log_to or timestamp <= log_to)):
                            result.write(line.encode())
                    else:
                        result.write(line.encode())
                line = f.readline()

    return result


def logging_send_entries(scheme: dict[str, Any]) -> Response:
    """
    Retrieve from the log file, and send in response, the entries matching the criteria specified in *scheme*.

    :param scheme: the criteria for filtering the records to be returned
    :return: file containing the log entries requested
    """
    # declare the return variable
    result: Response

    # initialize the error messages list
    errors: list[str] = []

    # obtain the logging level
    log_level: int = str_positional(source=scheme.get("log-level", "debug")[:1].upper(),
                                    list_origin=["debug", "info", "warning", "error", "critical"],
                                    list_dest=[10, 20, 30, 40, 50])
    # obtain the  timestamps
    log_from: datetime = datetime_parse(dt_str=scheme.get("log-from-datetime"))
    log_to: datetime = datetime_parse(dt_str=scheme.get("log-to-datetime"))

    if not log_from and not log_to:
        last_days: str = scheme.get("log-last-days", "0")
        last_hours: str = scheme.get("log-last-hours", "0")
        offset_days: int = int(last_days) if last_days.isdigit() else 0
        offset_hours: int = int(last_hours) if last_hours.isdigit() else 0
        if offset_days or offset_hours:
            log_from = datetime.now() - timedelta(days=offset_days,
                                                  hours=offset_hours)
    # retrieve the log entries
    log_entries: BytesIO = logging_get_entries(errors=errors,
                                               log_level=log_level,
                                               log_from=log_from,
                                               log_to=log_to)
    # errors ?
    if not errors:
        # no, return the log entries requested
        log_file = scheme.get("log-filename")
        log_entries.seek(0)
        result = send_file(path_or_file=log_entries,
                           mimetype="text/plain",
                           as_attachment=log_file is not None,
                           download_name=log_file)
    else:
        # yes, report the failure
        result = Response(response=json.dumps(obj={"errors": errors}),
                          status=400,
                          mimetype="application/json")

    return result


# @flask_app.route(rule="/logging",
#                  methods=["GET", "POST"])
def logging_service() -> Response:
    """
    Entry pointy for configuring and retrieving the execution log of the system.

    The *GET* operation has a set of optional criteria, used to filter the records to be returned.
    They are specified according to the pattern
    *log-filename=<string>&log-level=<debug|info|warning|error|critical>&
    log-from-datetime=YYYYMMDDhhmmss&log-to-datetime=YYYYMMDDhhmmss&log-last-days=<n>&log-last-hours=<n>>*:
        - *log-filename*: the filename for saving the downloaded the data (if omitted, browser displays the data)
        - *log-level*: the logging level of the entries (defaults to *info*)
        - *log-from-datetime*: the start timestamp
        - log-to-datetime*: the finish timestamp
        - *log-last-days*: how many days before current date
        - *log-last-hours*: how may hours before current time
    The *POST* operation configures and starts/restarts the logger.
    These are the optional query parameters:
        - *log-filepath*: path for the log file
        - *log-filemode*: the mode for log file opening (a- append, w- truncate)
        - *log-level*: the logging level (*debug*, *info*, *warning*, *error*, *critical*)
        - *log-format*: the information and formats to be written to the log
        - *log-style*: the style used for building the 'log-format' parameter
        - *log-datetime*: the format for displaying the date and time (defaults to YYYY-MM-DD HH:MM:SS)
    For omitted parameters, current existing parameter values are used, or obtained from environment variables.

    :return: the requested log data, on 'GET', and the operation status, on 'POST'
    """
    # register the request
    req_query: str = request.query_string.decode()
    PYPOMES_LOGGER.info(f"Request {request.path}?{req_query}")

    # obtain the request parameters
    scheme: dict[str, Any] = {}
    # attempt to retrieve the JSON data in body
    with contextlib.suppress(Exception):
        scheme.update(request.get_json())
    # obtain parameters in URL query
    scheme.update(request.values)


    # run the request
    result: Response
    if request.method == "GET":
        # filter out unknown parameters
        result = logging_send_entries(scheme=scheme)
    else:
        scheme = {key: value for key, value in scheme.items()
                  if key in ["log-filepath", "log-filemode", "log-level",
                             "log-format", "log-style", "log-datetime"]}
        # were valid configuration parameters provided ?
        if scheme:
            # yes
            logging_startup(scheme=scheme)
            result = Response(status=200)
        else:
            # no
            result = Response(response="No configuration parameters provided",
                              status=400)
    # log the response
    PYPOMES_LOGGER.info(f"Response {request.path}?{req_query}: {result}")

    return result


def __get_logging_level(level: int | Literal["debug", "info", "warning", "error", "critical"]) -> int:
    """
    Translate the log severity string *level* into the logging's internal severity value.

    :param level: the string log severity
    :return: the internal logging severity value
    """
    result: int
    if isinstance(level, int):
        result = level
    else:
        match level:
            case "debug":
                result = DEBUG          # 10
            case "info":
                result = INFO           # 20
            case "warning":
                result = WARNING        # 30
            case "error":
                result = ERROR          # 40
            case "critical":
                result = CRITICAL       # 50
            case _:
                result = NOTSET         # 0

    return result


def __write_to_output(msg: str,
                      output_dev: TextIO) -> None:

    # has the output device been defined ?
    if output_dev:
        # yes, write the message to it
        output_dev.write(msg)

        # is the output device 'stderr' ou 'stdout' ?
        if output_dev.name.startswith("<std"):
            # yes, skip to the next line
            output_dev.write("\n")


# initialize the logger
logging_startup()

