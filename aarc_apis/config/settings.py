import logging

LOGS_DIR = "logs"
APP_NAME = "aarch_apis"

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "root": {"level": logging.DEBUG, "handlers": ["console"]},
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": logging.DEBUG,
            "formatter": "detailed",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": logging.DEBUG,
            "formatter": "detailed",
            # 'filename': '' + APP_NAME.lower() + '.log',
            "filename": "{}/{}.log".format(LOGS_DIR, APP_NAME.lower()),
            "mode": "a",
            "maxBytes": 10485760,
            "backupCount": 5,
        },
    },
    "formatters": {
        "detailed": {
            "format": (
                "%(asctime)s %(name)-17s line:%(lineno)-4d "
                "%(levelname)-8s %(message)s"
            )
        },
        "with_filter": {
            "format": (
                "%(asctime)s %(name)-17s line:%(lineno)-4d "
                "%(levelname)-8s User: %(user)-35s %(message)s"
            )
        },
    },
}
