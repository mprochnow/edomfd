import functools
import logging.config
import queue

import dateutil.parser
import screeninfo

from edoevent import EDOStatus
from edojournal import EDOJournal
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

log = logging.getLogger(__name__)


if __name__ == '__main__':
    def event_cb(q: queue.Queue, event: dict):
        if event['event'] == 'Status':
            q.put(EDOStatus(event))
        else:
            timestamp = dateutil.parser.isoparse(event['timestamp'])
            log.debug(f"New event: {timestamp.isoformat()} - {event['event']}")

    status_queue = queue.Queue()

    # Needs to be called before Tk is initialized because it might mess with DPI awareness
    monitors = list(screeninfo.get_monitors())

    window = AppWindow(monitors, status_queue)

    journal = EDOJournal(functools.partial(event_cb, status_queue))
    journal.start()

    try:
        window.show()
    except KeyboardInterrupt:
        window.destroy()

    journal.stop()

    print("Bye!")
