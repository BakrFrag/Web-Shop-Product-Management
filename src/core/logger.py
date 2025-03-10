from logging.config import dictConfig

logging_config = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "level": "DEBUG",
        },
    },
    "loggers": {
        "web_shop": { 
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}

def setup_logger():
    """
    setup logging configuration
    """
    dictConfig(logging_config)