import json
import logging
import os.path
import pathlib
import re

from watchdog.events import FileCreatedEvent, FileSystemEventHandler, DirCreatedEvent, DirModifiedEvent, \
    FileModifiedEvent
from watchdog.observers import Observer

from windows import get_known_folder_path, FOLDERID_SavedGames

log = logging.getLogger(__name__)

REGEX_JOURNAL = re.compile(r'^Journal\.\d{4}-\d{2}-\d{2}T\d{6}\.\d{2}\.log$')
FILENAME_NAV_ROUTE = 'NavRoute.json'
FILENAME_STATUS = 'Status.json'


class EDOStatus:
    def __init__(self, j):
        flags = j['Flags']
        flags2 = j['Flags2']

        self.docked = flags & 0x01
        self.landed = flags & 0x02
        self.landing_gear = flags & 0x04
        self.shields_up = flags & 0x08
        self.supercruise = flags & 0x10
        self.flight_assist_off = flags & 0x20
        self.hardpoints_deployed = flags & 0x40
        self.in_wing = flags & 0x80
        self.lights_on = flags & 0x0100
        self.cargo_scoop_deployed = flags & 0x0200
        self.silent_running = flags & 0x0400
        self.scooping_fuel = flags & 0x0800
        self.srv_handbrake = flags & 0x1000
        self.srv_turret_view = flags & 0x2000
        self.srv_turret_retracted = flags & 0x4000
        self.srv_drive_assist = flags & 0x8000
        self.fsd_mass_locked = flags & 0x010000
        self.fsd_charging = flags & 0x020000
        self.fsd_cooldown = flags & 0x040000
        self.low_fuel = flags & 0x080000
        self.over_heating = flags & 0x100000
        self.has_lat_long = flags & 0x200000
        self.in_danger = flags & 0x400000
        self.being_interdicted = flags & 0x800000
        self.in_main_ship = flags & 0x01000000
        self.in_fighter = flags & 0x02000000
        self.in_srv = flags & 0x04000000
        self.analysis_mode = flags & 0x08000000
        self.night_vision = flags & 0x10000000
        self.altitude_from_average_radius = flags & 0x20000000
        self.fsd_jump = flags & 0x40000000
        self.srv_high_beam = flags & 0x80000000
        self.fsd_hyper_charging = flags2 & 0x080000


class EDOJournal(FileSystemEventHandler):
    def __init__(self, status_cb) -> None:
        self._status_cb = status_cb

        journal_dir = pathlib.Path(
            get_known_folder_path(FOLDERID_SavedGames)) / 'Frontier Developments' / 'Elite Dangerous'

        self._logdir = os.path.expanduser(journal_dir)

        log.debug(f"Observing {self._logdir}")

        self._observer = Observer()
        self._observer.schedule(self, self._logdir)

        self._load_status(os.path.expanduser(journal_dir / FILENAME_STATUS))

    def start(self) -> None:
        self._observer.start()

    def stop(self) -> None:
        self._observer.stop()
        self._observer.join()

    def on_created(self, event: DirCreatedEvent | FileCreatedEvent) -> None:
        if not event.is_directory:
            filename = os.path.basename(event.src_path)

    def on_modified(self, event: DirModifiedEvent | FileModifiedEvent) -> None:
        if not event.is_directory:
            filename = os.path.basename(event.src_path)

            if filename == FILENAME_STATUS:
                self._load_status(event.src_path)

    def _load_status(self, filename):
        with open(filename, 'rb', 0) as f:
            c = f.read().strip()
            if c:
                try:
                    self._status_cb(EDOStatus(json.loads(c)))
                except KeyError:
                    pass


