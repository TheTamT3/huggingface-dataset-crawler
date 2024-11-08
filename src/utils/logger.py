import logging
import os
from typing import Any

import coloredlogs


class EndpointFilter(logging.Filter):
    def __init__(
        self,
        path: str,
        *args: Any,
        **kwargs: Any,
    ):
        super().__init__(*args, **kwargs)
        self._path = path

    def filter(self, record: logging.LogRecord) -> bool:
        return record.getMessage().find(self._path) == -1


class ExactEndpointFilter(logging.Filter):
    def __init__(self, method: str, path: str, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self._method: str = method
        self._path: str = path

    def filter(self, record: logging.LogRecord) -> bool:
        record_method: str = record.args[1]  # type: ignore
        record_api_path: str = record.args[2]  # type: ignore
        return not (record_method == self._method and record_api_path == self._path)


def _set_colorlogs_env() -> None:
    os.environ[
        # "COLOREDLOGS_LOG_FORMAT"] = "%(asctime)s %(name)s %(levelname)5.5s   %(module)12.12s:%(lineno)3.3s - %(message)s"
        "COLOREDLOGS_LOG_FORMAT"
    ] = "%(asctime)s %(levelname)5.5s %(module)16.16s:%(lineno)3.3s - %(message)s"
    os.environ["COLOREDLOGS_FIELD_STYLES"] = ";".join(["asctime=green", "levelname=black,bold", "funcName=blue", "module=blue"])
    os.environ["COLOREDLOGS_LEVEL_STYLES"] = ";".join([
        "info=white",
        "debug=white",
        "warning=yellow",
        "success=118,bold",
        "error=red",
        "critical=background=red",
    ])
    os.environ["COLOREDLOGS_DATE_FORMAT"] = "%Y-%m-%d %H:%M:%S"


def configure_logger(level: str = "WARNING") -> None:
    level = level.upper()
    logging.getLogger("matplotlib").setLevel(logging.WARNING)
    logging.getLogger("elasticsearch").setLevel(logging.WARNING)
    logging.getLogger("sentry_sdk.errors").setLevel(logging.WARNING)

    loggers = ["root", "urllib3", "httpcore", "pymongo", "tzlocal", "googleapiclient", "apscheduler", "httpx"]
    for name in loggers:
        logger = logging.getLogger(name)
        logger.handlers.clear()
        logger.setLevel(level if name == "root" else logging.WARNING)

    # Disable logger fastAPI
    uvicorn_logger = logging.getLogger("uvicorn.access")
    uvicorn_logger.addFilter(EndpointFilter(path="/api/manage/health_check"))
    uvicorn_logger.addFilter(ExactEndpointFilter(method="GET", path="/"))

    # Disable logger for sentry
    sentry_logger = logging.getLogger("sentry_sdk.internal")
    sentry_logger.addFilter(EndpointFilter(path="/api/74"))

    _set_colorlogs_env()
    coloredlogs.install(level=level)
