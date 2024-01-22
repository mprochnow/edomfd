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


# class Event:
#     event: EventType
#
#
# class Location:
#     star_system: str
#     system_address: int
#     star_pos: int[int, int, int]
#     event: EventType = EventType.Location
#
#
# class NavRoute(Event):  # 1
#     class Route:
#         star_class: str
#         star_pos: int[int, int, int]
#         star_system: str
#         system_address: int
#
#     route: list[Route]
#     event: EventType = EventType.NavRoute
#
#
# class FSDTarget(Event):  # 2, 4
#     name: str
#     remaining_jumps_in_route: int
#     star_class: str
#     system_address: int
#     event: EventType = EventType.FSDTarget
#
#
# class StartJump(Event):  # 3, 6
#     jump_type: str
#     star_class: str
#     star_system: str
#     system_address: int
#     taxi: bool
#     event: EventType = EventType.StartJump
#
#
# class FSDJump(Event):  # 5, 8
#     body: str
#     body_id: int
#     body_type: str
#     conflicts: list[dict]
#     factions: list[dict]
#     fuel_level: float
#     fuel_used: float
#     jump_dist: float
#     multicrew: bool
#     population: int
#     star_pos: tuple[int, int, int]
#     star_system: str
#     system_address: int
#     system_allegiance: str
#     system_economy: str
#     system_economy_localized: str
#     system_faction: dict[str, str]
#     system_government: str
#     system_government_localized: str
#     system_second_economy: str
#     system_second_economy_localised: str
#     system_security: str
#     system_security_localised: str
#     taxi: bool
#     event: EventType = EventType.FSDJump
#
#
# class NavRouteClear(Event):  # 7
#     event: EventType = EventType.NavRouteClear


class Status:
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
