# Copyright (C) Martin J. Prochnow
# This file is part of EDOMFD <https://github.com/mprochnow/edomfd>.
#
# EDOMFD is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# EDOMFD is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with EDOMFD.  If not, see <http://www.gnu.org/licenses/>.

import logging
import msvcrt
import os.path
import pathlib
from types import TracebackType

import screeninfo
import tkinter as tk

import edoevent
import edostate
from edoevent import EventType
from edojournal import get_journal_dir, Journal
from ui.appwindow import AppWindow

LOCK_FILENAME = 'edomfd.lock'

log = logging.getLogger(__name__)


class WindowsFileLock:
    class Locked(Exception):
        pass

    def __init__(self, path: str) -> None:
        self._path: str = path
        self._fd: int | None = None

    def __enter__(self) -> 'WindowsFileLock':
        self._fd = os.open(self._path, os.O_RDWR | os.O_CREAT | os.O_TRUNC)
        try:
            msvcrt.locking(self._fd, msvcrt.LK_NBLCK, 1)
        except PermissionError:
            raise WindowsFileLock.Locked()

        return self

    def __exit__(
            self,
            exc_type: type[BaseException] | None,
            exc_value: BaseException | None,
            traceback: TracebackType | None,
    ) -> None:
        msvcrt.locking(self._fd, msvcrt.LK_UNLCK, 1)
        os.close(self._fd)
        pathlib.Path(self._path).unlink()


class Main:
    def __init__(self, journal_dir: str) -> None:
        # Needs to be called before Tk is initialized because it might mess with DPI awareness
        monitors = list(screeninfo.get_monitors())

        self._tk = tk.Tk()
        self._window = AppWindow(monitors, self._tk)

        self._current_state = edostate.CurrentState(journal_dir, self._event_cb)

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
                    0, self._window.status_panel.set, s.fsd_mass_locked, s.cargo_scoop_deployed, s.landing_gear,
                    s.hardpoints_deployed, s.lights_on, s.night_vision
                )
            case EventType.Location | EventType.FSDJump:
                self._tk.after(0, self._window.nav_route_panel.set_current_system, state.star_system[0])
                # TODO: Copy system name to clipboard?
            case EventType.NavRoute | EventType.FSDTarget | EventType.NavRouteClear:
                self._tk.after(0, self._window.nav_route_panel.set_current_system, state.star_system[0])
                self._tk.after(0, self._window.nav_route_panel.set_route, state.route)

            case EventType.Cargo | EventType.Loadout:
                self._tk.after(0, self._window.cargo_panel.set, *state.cargo_capacity, state.cargo_list)


if __name__ == '__main__':
    journal_dir = get_journal_dir()
    lock_file = os.path.join(journal_dir, LOCK_FILENAME)

    try:
        with WindowsFileLock(lock_file):
            Main(journal_dir)()
    except WindowsFileLock.Locked:
        print('Already running.')
