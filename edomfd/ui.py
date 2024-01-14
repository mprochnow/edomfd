import queue
from tkinter import *
from tkinter import ttk

import screeninfo

from edojournal import EDOStatus

QUEUE_CHECK_TIME = 100  # ms


class AppWindow:
    def __init__(self, monitors: list[screeninfo.Monitor], status_queue: queue.Queue):
        self._monitors: list[screeninfo.Monitor] = monitors
        self._status_queue: queue.Queue = status_queue

        self._fullscreen: bool = False

        self._tk = Tk()
        self._tk.title("EDO MFD")
        self._tk.columnconfigure(0, weight=3)
        self._tk.rowconfigure(0, weight=1)

        self._style = ttk.Style(self._tk)
        self._style.configure('TFrame', background='#000000')
        self._style.configure('Status.TLabel', background='#DE9A01')
        self._style.map('Status.TLabel',
                        background=[('disabled', '#000000')],
                        foreground=[('disabled', '#DE9A01')])

        self._frame = ttk.Frame(self._tk, relief='ridge')
        self._frame.grid(column=0, row=0, sticky="news")
        self._frame.columnconfigure(0, weight=1)
        self._frame.columnconfigure(1, weight=1)
        self._frame.columnconfigure(2, weight=1)

        self._label_docked = ttk.Label(self._frame, text="Docked", style='Status.TLabel')
        self._label_landed = ttk.Label(self._frame, text="Landed", style='Status.TLabel')
        self._label_landing_gear = ttk.Label(self._frame, text="Landing Gear", style='Status.TLabel')
        self._label_shields = ttk.Label(self._frame, text="Shields", style='Status.TLabel')
        self._label_supercruise = ttk.Label(self._frame, text="Supercruise", style='Status.TLabel')
        self._label_flight_assist_off = ttk.Label(self._frame, text="Flight Assist Off", style='Status.TLabel')
        self._label_hardpoints = ttk.Label(self._frame, text="Hardpoints", style='Status.TLabel')
        self._label_lights = ttk.Label(self._frame, text="Lights", style='Status.TLabel')
        self._label_night_vision = ttk.Label(self._frame, text="Night Vision", style='Status.TLabel')
        self._label_cargo_scoop = ttk.Label(self._frame, text="Cargo Scoop", style='Status.TLabel')
        self._label_silent_running = ttk.Label(self._frame, text="Silent Running", style='Status.TLabel')
        self._label_scooping_fuel = ttk.Label(self._frame, text="Scooping Fuel", style='Status.TLabel')
        self._label_fsd_mass_locked = ttk.Label(self._frame, text="FSD Mass-locked", style='Status.TLabel')
        self._label_fsd_charging = ttk.Label(self._frame, text="FSD Charging", style='Status.TLabel')
        self._label_fsd_hyper_charging = ttk.Label(self._frame, text="FSD Hyper-Drive Charging", style='Status.TLabel')
        self._label_fsd_jump = ttk.Label(self._frame, text="FSD Jump", style='Status.TLabel')
        self._label_fsd_cooldown = ttk.Label(self._frame, text="FSD Cooldown", style='Status.TLabel')
        self._label_hud_analysis_mode = ttk.Label(self._frame, text="Analysis Mode", style='Status.TLabel')

        self._tk.bind('<Escape>', self._close)
        self._tk.bind('<F11>', self._toggle_fullscreen)

        self._arrange_labels()
        self._maybe_move_to_secondary_monitor()
        self._tk.after(QUEUE_CHECK_TIME, self._update)

    def show(self):
        self._tk.mainloop()

    def destroy(self):
        self._tk.destroy()

    def _update(self):
        self._tk.after(QUEUE_CHECK_TIME, self._update)

        while not self._status_queue.empty():
            status: EDOStatus = self._status_queue.get_nowait()

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
                label.grid(column=i_col, row=i_row, padx=0, pady=0, sticky=N+E+S+W)

    def _maybe_move_to_secondary_monitor(self):
        for monitor in self._monitors:
            if not monitor.is_primary:
                self._tk.geometry(f"+{monitor.x:+}{monitor.y:+}")
                self._toggle_fullscreen()
                break

    def _close(self, event=None):
        self._tk.quit()

    def _toggle_fullscreen(self, event=None):
        self._fullscreen = not self._fullscreen

        if self._fullscreen:
            self._tk.update_idletasks()
            self._geometry = self._tk.geometry()
            # Tk.attribute("-fullscreen", True) always moves app window to the primary monitor.
            # This is a work-around for this behavior.
            self._tk.state('zoomed')
            self._tk.overrideredirect(True)
        else:
            self._tk.state('normal')
            self._tk.geometry(self._geometry)
            self._tk.overrideredirect(False)
