import logging
import logging.config


def setup_logging(log_level: str) -> None:
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError("Invalid log level: {0}".format(log_level))

    LOGGING_CONFIG = {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "standard": {"format": "%(asctime)s - %(levelname)s - %(filename)s - %(threadName)s - %(message)s"},
        },
        "handlers": {
            "default": {
                "level": log_level.upper(),
                "formatter": "standard",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            }
        },
        "loggers": {
            "": {
                "handlers": ["default"],
                "level": log_level.upper(),
                "propagate": False,
            },
        },
    }
    logging.config.dictConfig(LOGGING_CONFIG)
