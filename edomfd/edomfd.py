import logging.config

import screeninfo

from ui import AppWindow

logging.config.dictConfig({
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "custom": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    },
    "handlers": {
        "default": {
            "class": "logging.StreamHandler",
            "formatter": "custom"
        }
    },
    "loggers": {
        "": {
            "level": "DEBUG",
            "handlers": ["default"]
        }
    }
})


if __name__ == '__main__':
    # Needs to be called before Tk is initialized because it might mess with DPI awareness
    monitors = list(screeninfo.get_monitors())

    window = AppWindow(monitors)
    try:
        window.show()
    except KeyboardInterrupt:
        pass

    print("Bye!")
