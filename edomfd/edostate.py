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

import dataclasses
import json
import math
import os.path
from typing import Callable

import edoevent
import edojournal
from edoevent import EventType, StationType

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
        self._bounty: int = 0
        self._landing_pad: int | None = None

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

    @property
    def bounty(self) -> int:
        return self._bounty

    @property
    def landing_pad(self) -> int | None:
        return self._landing_pad

    def consume_event(self, event: dict) -> None:
        try:
            event_type: EventType = EventType(event['event'])
        except ValueError as e:
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
                try:
                    self._remaining_jumps_in_route = event['RemainingJumpsInRoute']
                except KeyError:
                    self._route.clear()
                    self._remaining_jumps_in_route = 0
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
            case EventType.Bounty:
                self._bounty += event.get('TotalReward', event.get('Reward', 0))
            case EventType.RedeemVoucher:
                if event['Type'] == 'bounty':
                    self._bounty = 0
            case EventType.DockingGranted:
                landing_pad = event['LandingPad']
                station_type = StationType(event['StationType'])

                if station_type in (
                     StationType.Coriolis, StationType.Orbis, StationType.Ocellus, StationType.AsteroidBase
                ):
                    if 1 <= landing_pad <= 45:
                        self._landing_pad = landing_pad
            case EventType.Docked | EventType.DockingTimeout:
                self._landing_pad = None

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
                            math.pow(route[i - 1]['StarPos'][0] - route[i]['StarPos'][0], 2) +
                            math.pow(route[i - 1]['StarPos'][1] - route[i]['StarPos'][1], 2) +
                            math.pow(route[i - 1]['StarPos'][2] - route[i]['StarPos'][2], 2)
                        )

                    route_entry = RouteEntry(
                        entry['SystemAddress'],
                        entry['StarSystem'],
                        entry['StarClass'],
                        StarPos(*entry['StarPos']),
                        distance
                    )

                    self._route.append(route_entry)

                self._remaining_jumps_in_route = len(self._route) - 1

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
                    try:
                        event_type = EventType(event['event'])
                    except ValueError:
                        continue

                    self._consume_event(event_type, event)
