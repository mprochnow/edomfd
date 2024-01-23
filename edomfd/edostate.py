import dataclasses
import json
import math
import os.path
from typing import Callable

import edoevent
import edojournal
from edoevent import EventType

FILENAME_NAV_ROUTE = 'NavRoute.json'
FILENAME_CARGO_LIST = 'Cargo.json'


@dataclasses.dataclass
class StarPos:
    x: float
    y: float
    z: float


@dataclasses.dataclass
class RouteEntry:
    system_address: int
    star_system: str
    star_class: str
    star_pos: StarPos
    distance: float


@dataclasses.dataclass
class CargoListEntry:
    name: str
    count: int


class CurrentState:
    def __init__(self, journal_dir: str, event_cb: Callable) -> None:
        self._journal_dir: str = journal_dir
        self._event_cb: Callable = event_cb

        self._status: edoevent.Status | None = None
        self._star_pos: StarPos | None = None
        self._star_system: str | None = None
        self._route: list[RouteEntry] = []
        self._remaining_jumps_in_route: int = 0
        self._cargo_list: list[CargoListEntry] = []
        self._cargo_capacity: int = 0
        self._cargo_count: int = 0

        self._load_nav_route()
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

    @property
    def cargo_list(self) -> list[CargoListEntry]:
        return self._cargo_list

    @property
    def cargo_capacity(self) -> tuple[int, int]:
        return self._cargo_count, self._cargo_capacity

    def consume_event(self, event: dict) -> None:
        try:
            event_type: EventType = EventType(event['event'])
        except ValueError as e:
            # print(event['event'])
            return

        self._consume_event(event_type, event)
        self._event_cb(self, event_type)

    def _consume_event(self, event_type: EventType, event: dict) -> None:
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
            case EventType.Loadout:
                self._cargo_capacity = event['CargoCapacity']
            case EventType.Cargo:
                self._load_cargo_list()

    def _load_nav_route(self) -> None:
        self._route.clear()

        filename: str = os.path.join(self._journal_dir, FILENAME_NAV_ROUTE)
        with open(filename, 'rb') as f:
            content: bytes = f.read().strip()
            if content:
                data: dict = json.loads(content)
                route: list[dict] = data['Route']

                for i, entry in enumerate(route):
                    distance: float = 0
                    if i > 0:
                        distance = math.sqrt(
                            math.pow(route[i-1]['StarPos'][0] - route[i]['StarPos'][0], 2) +
                            math.pow(route[i-1]['StarPos'][1] - route[i]['StarPos'][1], 2) +
                            math.pow(route[i-1]['StarPos'][2] - route[i]['StarPos'][2], 2)
                        )

                    route_entry = RouteEntry(
                        entry['SystemAddress'],
                        entry['StarSystem'],
                        entry['StarClass'],
                        StarPos(*entry['StarPos']),
                        distance
                    )

                    self._route.append(route_entry)

                self._remaining_jumps_in_route = len(self._route)-1

    def _load_cargo_list(self) -> None:
        self._cargo_list.clear()

        filename: str = os.path.join(self._journal_dir, FILENAME_CARGO_LIST)
        with open(filename, 'rb') as f:
            content: bytes = f.read().strip()
            if content:
                data: dict = json.loads(content)

                self._cargo_count = data['Count']

                for entry in data['Inventory']:
                    self._cargo_list.append(
                        CargoListEntry(entry.get('Name_Localised', entry['Name']).capitalize(), entry['Count'])
                    )

                self._cargo_list.sort(key=lambda x: x.name)

    def _load_newest_journal(self) -> None:
        filename = edojournal.get_filename_of_newest_journal(self._journal_dir)
        if filename:
            with open(filename, 'rb') as f:
                for line in f:
                    event = json.loads(line)
                    event_type = event['event']
                    if event_type in ('Location', 'FSDJump', 'Loadout', 'Cargo'):
                        self._consume_event(EventType(event_type), event)
