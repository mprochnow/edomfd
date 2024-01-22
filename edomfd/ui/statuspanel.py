import tkinter as tk
from tkinter import ttk


class StatusPanel(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        self._label_docked = ttk.Label(self, text="Docked")
        self._label_landed = ttk.Label(self, text="Landed")
        self._label_landing_gear = ttk.Label(self, text="Landing Gear")
        self._label_shields = ttk.Label(self, text="Shields")
        self._label_supercruise = ttk.Label(self, text="Supercruise")
        self._label_flight_assist_off = ttk.Label(self, text="Flight Assist Off")
        self._label_hardpoints = ttk.Label(self, text="Hardpoints")
        self._label_lights = ttk.Label(self, text="Lights")
        self._label_night_vision = ttk.Label(self, text="Night Vision")
        self._label_cargo_scoop = ttk.Label(self, text="Cargo Scoop")
        self._label_silent_running = ttk.Label(self, text="Silent Running")
        self._label_fuel_scooping = ttk.Label(self, text="Fuel Scooping")
        self._label_fsd_mass_locked = ttk.Label(self, text="FSD Mass-locked")
        self._label_fsd_charging = ttk.Label(self, text="FSD Charging")
        self._label_fsd_hyper_charging = ttk.Label(self, text="FSD Hyper-Drive Charging")
        self._label_fsd_jump = ttk.Label(self, text="FSD Jump")
        self._label_fsd_cooldown = ttk.Label(self, text="FSD Cooldown")
        self._label_hud_analysis_mode = ttk.Label(self, text="Analysis Mode")

        self._arrange_labels()

    def set(self, docked: bool, landed: bool, landing_gear: bool, shields: bool, supercruise: bool,
            flight_assist_off: bool, hardpoints_deployed: bool, lights: bool, night_vision: bool,
            cargo_scoop_deployed: bool, silent_running: bool, fuel_scooping: bool, fsd_mass_locked: bool,
            fsd_charging: bool, fsd_hyper_drive_charging: bool, fsd_jump: bool, fsd_cooldown: bool,
            analysis_mode: bool) -> None:
        self._label_docked.configure(state='enabled' if docked else 'disabled')
        self._label_landed.configure(state='enabled' if landed else 'disabled')
        self._label_landing_gear.configure(state='enabled' if landing_gear else 'disabled')
        self._label_shields.configure(state='enabled' if shields else 'disabled')
        self._label_supercruise.configure(state='enabled' if supercruise else 'disabled')
        self._label_flight_assist_off.configure(state='enabled' if flight_assist_off else 'disabled')
        self._label_hardpoints.configure(state='enabled' if hardpoints_deployed else 'disabled')
        self._label_lights.configure(state='enabled' if lights else 'disabled')
        self._label_night_vision.configure(state='enabled' if night_vision else 'disabled')
        self._label_cargo_scoop.configure(state='enabled' if cargo_scoop_deployed else 'disabled')
        self._label_silent_running.configure(state='enabled' if silent_running else 'disabled')
        self._label_fuel_scooping.configure(state='enabled' if fuel_scooping else 'disabled')
        self._label_fsd_mass_locked.configure(state='enabled' if fsd_mass_locked else 'disabled')
        self._label_fsd_charging.configure(state='enabled' if fsd_charging else 'disabled')
        self._label_fsd_hyper_charging.configure(state='enabled' if fsd_hyper_drive_charging else 'disabled')
        self._label_fsd_jump.configure(state='enabled' if fsd_jump else 'disabled')
        self._label_fsd_cooldown.configure(state='enabled' if fsd_cooldown else 'disabled')
        self._label_hud_analysis_mode.configure(state='enabled' if analysis_mode else 'disabled')

    def _arrange_labels(self):
        labels = [
            [self._label_docked, self._label_landed, self._label_hud_analysis_mode],
            [self._label_shields, self._label_silent_running, self._label_flight_assist_off],
            [self._label_hardpoints, self._label_cargo_scoop, self._label_landing_gear],
            [self._label_lights, self._label_night_vision, self._label_fuel_scooping],
            [self._label_fsd_charging, self._label_fsd_hyper_charging, self._label_fsd_cooldown],
            [self._label_fsd_mass_locked, self._label_fsd_jump, self._label_supercruise]
        ]

        for i_row, row in enumerate(labels):
            for i_col, label in enumerate(row):
                label.configure(state='disabled')
                label.grid(column=i_col, row=i_row, padx=1, pady=1, sticky=tk.N+tk.E+tk.S+tk.W)
