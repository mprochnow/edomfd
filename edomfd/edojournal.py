import json
import logging
import os.path
import pathlib
import re
from os import SEEK_SET, SEEK_END
from typing import Callable, BinaryIO

from watchdog.events import FileCreatedEvent, FileSystemEventHandler, DirCreatedEvent, DirModifiedEvent, \
    FileModifiedEvent
from watchdog.observers import Observer

from windows import get_known_folder_path, FOLDERID_SavedGames

log = logging.getLogger(__name__)

REGEX_JOURNAL = re.compile(r'^Journal\.\d{4}-\d{2}-\d{2}T\d{6}\.\d{2}\.log$')
FILENAME_NAV_ROUTE = 'NavRoute.json'
FILENAME_STATUS = 'Status.json'


class EDOJournal(FileSystemEventHandler):
    def __init__(self, event_cb: Callable) -> None:
        self._event_cb: Callable = event_cb

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
        if not event.is_directory:
            filename = os.path.basename(event.src_path)

            if REGEX_JOURNAL.match(filename):
                self._journal_created(event.src_path)

    def on_modified(self, event: DirModifiedEvent | FileModifiedEvent) -> None:
        if not event.is_directory:
            filename = os.path.basename(event.src_path)

            if filename == FILENAME_STATUS:
                self._load_status(event.src_path)
            elif REGEX_JOURNAL.match(filename):
                self._journal_update(event.src_path)

    def _load_status(self, filename: str) -> None:
        with open(filename, 'rb', 0) as f:
            line = f.read().strip()
            if line:
                self._event_cb(json.loads(line))

    def _journal_created(self, filename: str) -> None:
        log.debug(f"New journal {os.path.basename(filename)}")

        self._journal_filename = filename

        if self._journal_file:
            self._journal_file.close()
            self._journal_pos = -1

        self._journal_file = open(self._journal_filename, 'rb', 0)
        self._read_journal()

    def _journal_update(self, filename: str) -> None:
        if self._journal_file is None:
            self._journal_filename = filename
            self._journal_file = open(self._journal_filename, 'rb', 0)

        self._read_journal()

    def _read_journal(self):
        if self._journal_pos >= 0:
            self._journal_file.seek(self._journal_pos, SEEK_SET)

        for line in self._journal_file:
            self._event_cb(json.loads(line))

        self._journal_pos = self._journal_file.tell()

    def _get_journal_newest_filename(self) -> str | None:
        journal_files = (x for x in os.listdir(self._journal_dir) if REGEX_JOURNAL.search(x))
        if journal_files:
            journals_dir_path = pathlib.Path(self._journal_dir)
            journal_files = (journals_dir_path / pathlib.Path(x) for x in journal_files)
            return str(max(journal_files, key=os.path.getctime))

        return None
