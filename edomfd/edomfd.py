import logging

import screeninfo
import tkinter as tk

import edoevent
import edostate
from edoevent import EventType
from edojournal import get_journal_dir, Journal
from ui import AppWindow

log = logging.getLogger(__name__)


class Main:
    def __init__(self):
        # Needs to be called before Tk is initialized because it might mess with DPI awareness
        monitors = list(screeninfo.get_monitors())

        self._tk = tk.Tk()
        self._window = AppWindow(monitors, self._tk)

        self._current_state = edostate.CurrentState(get_journal_dir(), self._event_cb)

        self._journal = Journal(self._current_state.consume_event)

    def __call__(self):
        self._journal.start()

        self._tk.after(0, self._window.nav_route_panel.set_current_system, self._current_state.star_system[0])
        self._tk.after(0, self._window.nav_route_panel.set_route, self._current_state.route)
        self._tk.after(0, self._window.cargo_panel.set, *self._current_state.cargo_capacity,
                       self._current_state.cargo_list)

        try:
            self._window.show()
        except KeyboardInterrupt:
            self._window.destroy()

        self._journal.stop()

        log.debug("Bye!")

    def _event_cb(self, state: edostate.CurrentState, event_type: EventType):
        match event_type:
            case EventType.Status:
                s: edoevent.Status = state.status

                self._tk.after(
                    0, self._window.status_panel.set, s.docked, s.landed, s.landing_gear, s.shields_up, s.supercruise,
                    s.flight_assist_off, s.hardpoints_deployed, s.lights_on, s.night_vision, s.cargo_scoop_deployed,
                    s.silent_running, s.scooping_fuel, s.fsd_mass_locked, s.fsd_charging, s.fsd_hyper_charging,
                    s.fsd_jump, s.fsd_cooldown, s.analysis_mode
                )

                self._tk.after(0, self._window.geocoordinates_panel.set, s.latitude, s.longitude, s.heading, s.altitude)
            case EventType.Location:
                self._tk.after(0, self._window.nav_route_panel.set_current_system, state.star_system[0])
            case EventType.NavRoute | EventType.FSDTarget | EventType.NavRouteClear:
                self._tk.after(0, self._window.nav_route_panel.set_current_system, state.star_system[0])
                self._tk.after(0, self._window.nav_route_panel.set_route, state.route)

            case EventType.Cargo | EventType.Loadout:
                self._tk.after(0, self._window.cargo_panel.set, *state.cargo_capacity, state.cargo_list)

            # case EventType.Bounty | EventType.RedeemVoucher:
            #     self._tk.after(0, self._window.bounty_panel.set, state.bounty)


if __name__ == '__main__':
    Main()()
