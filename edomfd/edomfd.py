import functools
import logging.config
import pprint

import screeninfo

import edoevent
import edostate
from edoevent import EventType
from edojournal import get_journal_dir, Journal
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
    def event_cb(win: AppWindow, state: edostate.CurrentState, event_type: EventType):
        match event_type:
            case EventType.Status:
                s: edoevent.Status = state.status

                win.tk.after(
                    0, win.status_panel.set, s.docked, s.landed, s.landing_gear, s.shields_up, s.supercruise,
                    s.flight_assist_off, s.hardpoints_deployed, s.lights_on, s.night_vision, s.cargo_scoop_deployed,
                    s.silent_running, s.scooping_fuel, s.fsd_mass_locked, s.fsd_charging, s.fsd_hyper_charging,
                    s.fsd_jump, s.fsd_cooldown, s.analysis_mode
                )

                win.tk.after(0, win.geocoordinates_panel.set, s.latitude, s.longitude, s.heading, s.altitude)
            case EventType.NavRoute | EventType.FSDTarget:
                pprint.pprint(state.route)
            case EventType.FSDJump:
                print(state.star_system)

    # Needs to be called before Tk is initialized because it might mess with DPI awareness
    monitors = list(screeninfo.get_monitors())

    window = AppWindow(monitors)

    current_state = edostate.CurrentState(get_journal_dir(), functools.partial(event_cb, window))

    journal = Journal(current_state.consume_event)
    journal.start()

    try:
        window.show()
    except KeyboardInterrupt:
        window.destroy()

    journal.stop()

    print("Bye!")
