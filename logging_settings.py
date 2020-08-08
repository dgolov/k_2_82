# Настройки логирования

import logging
import logging.config


log_config = {
    "version": 1,
    "formatters": {
        "formatter": {
            "format": "%(asctime)s - %(levelname)s - %(message)s"
        },
    },
    "handlers": {
        "file_handler": {
            "class": "logging.FileHandler",
            "formatter": "formatter",
            "filename": "events.log"
        },
    },
    "loggers": {
        "event": {
            "handlers": ["file_handler"],
            "level": "DEBUG",
        }
    },
}

logging.config.dictConfig(log_config)
event_log = logging.getLogger('event')