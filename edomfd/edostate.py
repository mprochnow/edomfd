import dataclasses
import json
import os.path
from typing import Callable

import edoevent
import edojournal
from edoevent import EventType

FILENAME_NAV_ROUTE = 'NavRoute.json'


@dataclasses.dataclass
class StarPos:
    x: float
    y: float
    z: float


@dataclasses.dataclass
class RouteEntry:
    star_system: str
    star_class: str
    star_pos: StarPos


class CurrentState:
    def __init__(self, journal_dir: str, event_cb: Callable) -> None:
        self._journal_dir: str = journal_dir
        self._event_cb: Callable = event_cb

        self._status: edoevent.Status | None = None
        self._star_pos: StarPos | None = None
        self._star_system: str | None = None
        self._route: list[RouteEntry] = []
        self._remaining_jumps_in_route: int = 0

        self._load_newest_journal()

    @property
    def status(self) -> edoevent.Status:
        return self._status

    @property
    def route(self) -> list[RouteEntry]:
        return self._route[-self._remaining_jumps_in_route:]

    @property
    def star_system(self) -> tuple[str, StarPos]:
        return self._star_system, self._star_pos

    def consume_event(self, event: dict) -> None:
        try:
            event_type: EventType = EventType(event['event'])
        except ValueError as e:
            return

        self._consume_event(event_type, event)
        self._event_cb(self, event_type)

    def _consume_event(self, event_type: EventType, event: dict):
        match event_type:
            case EventType.Status:
                self._status = edoevent.Status(event)
            case EventType.Location:
                self._star_system = event['StarSystem']
                self._star_pos = StarPos(*event['StarPos'])
            case EventType.NavRoute:
                self._load_nav_route()
            case EventType.FSDTarget:
                self._remaining_jumps_in_route = event['RemainingJumpsInRoute']
            case EventType.NavRouteClear:
                self._route.clear()
                self._remaining_jumps_in_route = 0
            case EventType.FSDJump:
                self._star_system = event['StarSystem']
                self._star_pos = StarPos(*event['StarPos'])

    def _load_nav_route(self) -> None:
        """
        File also contains current system!

        distance = sqrt( (x2 - x1)² + (y2 - y1)² + (z2 - z1)² )

        x1, y1, z1 is your source, or where you are starting from. x2, y2, z2 is destination
        """
        filename: str = os.path.join(self._journal_dir, FILENAME_NAV_ROUTE)
        with open(filename, 'rb') as f:
            content: bytes = f.read().strip()
            if content:
                data: dict = json.loads(content)

                for entry in data['Route']:
                    route_entry = RouteEntry(entry['StarSystem'], entry['StarClass'], StarPos(*entry['StarPos']))
                    self._route.append(route_entry)

                self._remaining_jumps_in_route = len(self._route)

    def _load_newest_journal(self):
        filename = edojournal.get_filename_of_newest_journal(self._journal_dir)
        if filename:
            with open(filename, 'rb') as f:
                for line in f:
                    event = json.loads(line)
                    event_type = event['event']
                    if event_type in ('Location', 'FSDJump'):
                        self._consume_event(EventType(event_type), event)
