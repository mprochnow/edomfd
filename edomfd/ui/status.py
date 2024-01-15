import tkinter as tk
from tkinter import ttk

from edojournal import EDOStatus


class StatusFrame(ttk.Frame):
    def __init__(self, parent, **kwargs):
        self._set_styles()

        kwargs['style'] = 'Status.TFrame'
        super().__init__(parent, **kwargs)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        self._label_docked = ttk.Label(self, text="Docked", style='Status.TLabel')
        self._label_landed = ttk.Label(self, text="Landed", style='Status.TLabel')
        self._label_landing_gear = ttk.Label(self, text="Landing Gear", style='Status.TLabel')
        self._label_shields = ttk.Label(self, text="Shields", style='Status.TLabel')
        self._label_supercruise = ttk.Label(self, text="Supercruise", style='Status.TLabel')
        self._label_flight_assist_off = ttk.Label(self, text="Flight Assist Off", style='Status.TLabel')
        self._label_hardpoints = ttk.Label(self, text="Hardpoints", style='Status.TLabel')
        self._label_lights = ttk.Label(self, text="Lights", style='Status.TLabel')
        self._label_night_vision = ttk.Label(self, text="Night Vision", style='Status.TLabel')
        self._label_cargo_scoop = ttk.Label(self, text="Cargo Scoop", style='Status.TLabel')
        self._label_silent_running = ttk.Label(self, text="Silent Running", style='Status.TLabel')
        self._label_scooping_fuel = ttk.Label(self, text="Scooping Fuel", style='Status.TLabel')
        self._label_fsd_mass_locked = ttk.Label(self, text="FSD Mass-locked", style='Status.TLabel')
        self._label_fsd_charging = ttk.Label(self, text="FSD Charging", style='Status.TLabel')
        self._label_fsd_hyper_charging = ttk.Label(self, text="FSD Hyper-Drive Charging", style='Status.TLabel')
        self._label_fsd_jump = ttk.Label(self, text="FSD Jump", style='Status.TLabel')
        self._label_fsd_cooldown = ttk.Label(self, text="FSD Cooldown", style='Status.TLabel')
        self._label_hud_analysis_mode = ttk.Label(self, text="Analysis Mode", style='Status.TLabel')

        self._arrange_labels()

    def update_status(self, status: EDOStatus):
        self._label_docked.configure(state='enabled' if status.docked else 'disabled')
        self._label_landed.configure(state='enabled' if status.landed else 'disabled')
        self._label_landing_gear.configure(state='enabled' if status.landing_gear else 'disabled')
        self._label_shields.configure(state='enabled' if status.shields_up else 'disabled')
        self._label_supercruise.configure(state='enabled' if status.supercruise else 'disabled')
        self._label_flight_assist_off.configure(state='enabled' if status.flight_assist_off else 'disabled')
        self._label_hardpoints.configure(state='enabled' if status.hardpoints_deployed else 'disabled')
        self._label_lights.configure(state='enabled' if status.lights_on else 'disabled')
        self._label_night_vision.configure(state='enabled' if status.night_vision else 'disabled')
        self._label_cargo_scoop.configure(state='enabled' if status.cargo_scoop_deployed else 'disabled')
        self._label_silent_running.configure(state='enabled' if status.silent_running else 'disabled')
        self._label_scooping_fuel.configure(state='enabled' if status.scooping_fuel else 'disabled')
        self._label_fsd_mass_locked.configure(state='enabled' if status.fsd_mass_locked else 'disabled')
        self._label_fsd_charging.configure(state='enabled' if status.fsd_charging else 'disabled')
        self._label_fsd_hyper_charging.configure(state='enabled' if status.fsd_hyper_charging else 'disabled')
        self._label_fsd_jump.configure(state='enabled' if status.fsd_jump else 'disabled')
        self._label_fsd_cooldown.configure(state='enabled' if status.fsd_cooldown else 'disabled')
        self._label_hud_analysis_mode.configure(state='enabled' if status.analysis_mode else 'disabled')

    def _arrange_labels(self):
        labels = [
            [self._label_docked, self._label_landed, self._label_hud_analysis_mode],
            [self._label_shields, self._label_silent_running, self._label_flight_assist_off],
            [self._label_hardpoints, self._label_cargo_scoop, self._label_landing_gear],
            [self._label_lights, self._label_night_vision, self._label_scooping_fuel],
            [self._label_fsd_charging, self._label_fsd_hyper_charging, self._label_fsd_cooldown],
            [self._label_fsd_mass_locked, self._label_fsd_jump, self._label_supercruise]
        ]

        for i_row, row in enumerate(labels):
            for i_col, label in enumerate(row):
                label.configure(state='disabled')
                label.grid(column=i_col, row=i_row, padx=1, pady=1, sticky=tk.N+tk.E+tk.S+tk.W)

    def _set_styles(self):
        self._style = ttk.Style()
        self._style.configure('Status.TFrame', background='#DE9A01')
        self._style.configure('Status.TLabel', background='#DE9A01')
        self._style.map('Status.TLabel',
                        background=[('disabled', '#000000')],
                        foreground=[('disabled', '#DE9A01')])
