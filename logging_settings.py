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