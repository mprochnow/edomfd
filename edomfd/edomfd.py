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
    def event_cb(win: AppWindow, event: dict):
        if event['event'] == 'Status':
            status = EDOStatus(event)

            win.tk.after(
                1,
                win.status_panel.set,
                status.docked, status.landed, status.landing_gear, status.shields_up, status.supercruise,
                status.flight_assist_off, status.hardpoints_deployed, status.lights_on, status.night_vision,
                status.cargo_scoop_deployed, status.silent_running, status.scooping_fuel, status.fsd_mass_locked,
                status.fsd_charging, status.fsd_hyper_charging, status.fsd_jump, status.fsd_cooldown,
                status.analysis_mode
            )

            win.tk.after(
                1,
                win.geocoordinates_panel.set,
                status.latitude,
                status.longitude,
                status.heading,
                status.altitude
            )
        else:
            timestamp = dateutil.parser.isoparse(event['timestamp'])
            log.debug(f"New event: {timestamp.isoformat()} - {event['event']}")

    # Needs to be called before Tk is initialized because it might mess with DPI awareness
    monitors = list(screeninfo.get_monitors())

    window = AppWindow(monitors)

    journal = EDOJournal(functools.partial(event_cb, window))
    journal.start()

    try:
        window.show()
    except KeyboardInterrupt:
        window.destroy()

    journal.stop()

    print("Bye!")
