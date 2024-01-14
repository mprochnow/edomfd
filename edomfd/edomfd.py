import functools
import logging.config
import queue

import screeninfo

from edojournal import EDOJournal, EDOStatus
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
    def status_cb(q: queue.Queue, status: EDOStatus):
        q.put(status)

    status_queue = queue.Queue()

    # Needs to be called before Tk is initialized because it might mess with DPI awareness
    monitors = list(screeninfo.get_monitors())

    window = AppWindow(monitors, status_queue)

    journal = EDOJournal(functools.partial(status_cb, status_queue))
    journal.start()

    try:
        window.show()
    except KeyboardInterrupt:
        window.destroy()

    journal.stop()

    print("Bye!")
