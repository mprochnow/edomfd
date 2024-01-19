import json
import logging
import os.path
import pathlib
import re
from os import SEEK_SET, SEEK_END
from typing import Callable, BinaryIO

import dateutil.parser
import dateutil.tz
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
        self.latitude = j.get('Latitude')
        self.longitude = j.get('Longitude')
        self.heading = j.get('Heading')
        self.altitude = j.get('Altitude')
        flags = j.get('Flags', 0)
        flags2 = j.get('Flags2', 0)

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
    def __init__(self, status_cb: Callable) -> None:
        self._status_cb: Callable = status_cb

        journal_dir = pathlib.Path(
            get_known_folder_path(FOLDERID_SavedGames)) / 'Frontier Developments' / 'Elite Dangerous'

        self._journal_dir = os.path.expanduser(journal_dir)
        self._journal_filename: str | None = self._get_journal_newest_filename()
        self._journal_file: BinaryIO | None = None
        self._journal_pos = -1

        self._observer = Observer()
        self._observer.schedule(self, self._journal_dir)

        self._load_status(os.path.join(self._journal_dir, FILENAME_STATUS))

        if self._journal_filename:
            self._journal_file = open(self._journal_filename, 'rb', 0)
            self._journal_file.seek(0, SEEK_END)
            self._journal_pos = self._journal_file.tell()

    def start(self) -> None:
        self._observer.start()

        log.debug(f"Started observing {self._journal_dir}")

    def stop(self) -> None:
        self._observer.stop()
        self._observer.join()

        if self._journal_file:
            self._journal_file.close()

        log.debug(f"Stopped observing {self._journal_dir}")

    def on_created(self, event: DirCreatedEvent | FileCreatedEvent) -> None:
        if event.is_directory:
            return

        filename = os.path.basename(event.src_path)

        if REGEX_JOURNAL.match(filename):
            self._journal_created(event.src_path)

    def on_modified(self, event: DirModifiedEvent | FileModifiedEvent) -> None:
        if event.is_directory:
            return

        filename = os.path.basename(event.src_path)

        if filename == FILENAME_STATUS:
            self._load_status(event.src_path)
        elif REGEX_JOURNAL.match(filename):
            self._journal_update(event.src_path)

    def _get_journal_newest_filename(self) -> str | None:
        journal_files = (x for x in os.listdir(self._journal_dir) if REGEX_JOURNAL.search(x))
        if journal_files:
            journals_dir_path = pathlib.Path(self._journal_dir)
            journal_files = (journals_dir_path / pathlib.Path(x) for x in journal_files)
            return str(max(journal_files, key=os.path.getctime))

        return None

    def _journal_created(self, filename: str) -> None:
        log.debug(f"New journal {os.path.basename(filename)}")

        if self._journal_file:
            self._journal_file.close()
            self._journal_file = None
            self._journal_pos = -1

        self._journal_filename = filename
        self._journal_file = open(self._journal_filename, 'rb', 0)
        self._read_journal()

    def _journal_update(self, filename: str) -> None:
        if self._journal_file is None:
            self._journal_filename = filename
            self._journal_file = open(self._journal_filename, 'rb', 0)

        self._read_journal()

    def _load_status(self, filename: str) -> None:
        with open(filename, 'rb', 0) as f:
            line = f.read().strip()
            if line:
                self._status_cb(EDOStatus(json.loads(line)))

    def _read_journal(self):
        if self._journal_pos >= 0:
            self._journal_file.seek(self._journal_pos, SEEK_SET)

        for line in self._journal_file:
            self._parse_line(line)

        self._journal_pos = self._journal_file.tell()

    def _parse_line(self, line: bytes):
        entry = json.loads(line)

        timestamp = dateutil.parser.isoparse(entry['timestamp'])
        log.debug(f"New event: {timestamp.isoformat()} - {entry['event']}")
