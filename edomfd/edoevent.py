# Copyright (C) Martin J. Prochnow
# Licensed under the GNU General Public License v3
# See LICENSE.MD

import enum


class EventType(enum.Enum):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return name

    Status = enum.auto()
    Location = enum.auto()
    NavRoute = enum.auto()  # Only raised once when route is plotted
    NavRouteClear = enum.auto()  # Raised before 'FSDJump' for last target in nav route
    FSDTarget = enum.auto()  # Raised before 'FSDJump'
    StartJump = enum.auto()  # Raised before 'FSDTarget'
    FSDJump = enum.auto()  # Last of this in journal contains current star pos
    Loadout = enum.auto()
    Cargo = enum.auto()
    Bounty = enum.auto()
    RedeemVoucher = enum.auto()
    DockingGranted = enum.auto()
    DockingDenied = enum.auto()
    DockingTimeout = enum.auto()
    Docked = enum.auto()


class StationType(enum.Enum):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return name

    Coriolis = enum.auto()
    Orbis = enum.auto()
    Ocellus = enum.auto()
    AsteroidBase = enum.auto()
    Outpost = enum.auto()
    MegaShip = enum.auto()
    FleetCarrier = enum.auto()
    CraterOutpost = enum.auto()
    OnFootSettlement = enum.auto()
    SpaceConstructionDepot = enum.auto()
    CraterPort = enum.auto()


class Status:
    def __init__(self, j):
        self.latitude: float | None = j.get('Latitude')
        self.longitude: float | None = j.get('Longitude')
        self.heading: float | None = j.get('Heading')
        self.altitude: float | None = j.get('Altitude')
        self.oxygen: float | None = j.get('Oxygen')
        self.gravity: float | None = j.get('Gravity')

        flags = j.get('Flags', 0)
        flags2 = j.get('Flags2', 0)

        self.docked = bool(flags & 0x01)
        self.landed = bool(flags & 0x02)
        self.landing_gear = bool(flags & 0x04)
        self.shields_up = bool(flags & 0x08)
        self.supercruise = bool(flags & 0x10)
        self.flight_assist_off = bool(flags & 0x20)
        self.hardpoints_deployed = bool(flags & 0x40)
        self.in_wing = bool(flags & 0x80)
        self.lights_on = bool(flags & 0x0100)
        self.cargo_scoop_deployed = bool(flags & 0x0200)
        self.silent_running = bool(flags & 0x0400)
        self.scooping_fuel = bool(flags & 0x0800)
        self.srv_handbrake = bool(flags & 0x1000)
        self.srv_turret_view = bool(flags & 0x2000)
        self.srv_turret_retracted = bool(flags & 0x4000)
        self.srv_drive_assist = bool(flags & 0x8000)
        self.fsd_mass_locked = bool(flags & 0x010000)
        self.fsd_charging = bool(flags & 0x020000)
        self.fsd_cooldown = bool(flags & 0x040000)
        self.low_fuel = bool(flags & 0x080000)
        self.over_heating = bool(flags & 0x100000)
        self.has_lat_long = bool(flags & 0x200000)
        self.in_danger = bool(flags & 0x400000)
        self.being_interdicted = bool(flags & 0x800000)
        self.in_main_ship = bool(flags & 0x01000000)
        self.in_fighter = bool(flags & 0x02000000)
        self.in_srv = bool(flags & 0x04000000)
        self.analysis_mode = bool(flags & 0x08000000)
        self.night_vision = bool(flags & 0x10000000)
        self.altitude_from_average_radius = bool(flags & 0x20000000)
        self.fsd_jump = bool(flags & 0x40000000)
        self.srv_high_beam = bool(flags & 0x80000000)

        self.on_foot = bool(flags2 & 0x01)
        self.in_taxi = bool(flags2 & 0x02)
        self.on_foot_in_station = bool(flags2 & 0x08)
        self.on_foot_on_planet = bool(flags2 & 0x0010)
        self.on_foot_in_hangar = bool(flags2 & 0x02000)
        self.on_foot_social_space = bool(flags2 & 0x04000)
        self.on_foot_exterior = bool(flags2 & 0x08000)  # Within station or building
        self.fsd_hyper_charging = bool(flags2 & 0x080000)
