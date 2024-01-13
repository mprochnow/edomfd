from tkinter import *
from tkinter import ttk

import screeninfo


class AppWindow:
    def __init__(self, monitors: list[screeninfo.Monitor]):
        self._fullscreen: bool = False

        self._tk = Tk()
        self._tk.title("EDO MFD")
        self._tk.columnconfigure(0, weight=3)
        self._tk.rowconfigure(0, weight=1)

        self._monitors = monitors

        self._frame = ttk.Frame(self._tk, relief='ridge')
        self._frame.grid(column=0, row=0, sticky="news")
        self._frame.columnconfigure(0, weight=1)
        self._frame.columnconfigure(1, weight=1)
        self._frame.columnconfigure(2, weight=1)

        self._label_docked = ttk.Label(self._frame, text="Docked")
        self._label_landed = ttk.Label(self._frame, text="Landed")
        self._label_landing_gear = ttk.Label(self._frame, text="Landing Gear")
        self._label_shields = ttk.Label(self._frame, text="Shields")
        self._label_supercruise = ttk.Label(self._frame, text="Supercruise")
        self._label_flight_assist_off = ttk.Label(self._frame, text="Flight Assist Off")
        self._label_hardpoints = ttk.Label(self._frame, text="Hardpoints")
        self._label_lights = ttk.Label(self._frame, text="Lights")
        self._label_night_vision = ttk.Label(self._frame, text="Night Vision")
        self._label_cargo_scoop = ttk.Label(self._frame, text="Cargo Scoop")
        self._label_silent_running = ttk.Label(self._frame, text="Silent Running")
        self._label_scooping_fuel = ttk.Label(self._frame, text="Scooping Fuel")
        self._label_fsd_mass_locked = ttk.Label(self._frame, text="FSD Mass-locked")
        self._label_fsd_charging = ttk.Label(self._frame, text="FSD Charging")
        self._label_fsd_hyper_charging = ttk.Label(self._frame, text="FSD Hyper-Drive Charging")
        self._label_fsd_jump = ttk.Label(self._frame, text="FSD Jump")
        self._label_fsd_cooldown = ttk.Label(self._frame, text="FSD Cooldown")
        self._label_hud_analysis_mode = ttk.Label(self._frame, text="Analysis Mode")

        self._tk.bind('<Escape>', self._close)
        self._tk.bind('<F11>', self._toggle_fullscreen)

        self._arrange_labels()
        self._maybe_move_to_secondary_monitor()

    def show(self):
        self._tk.mainloop()

    def _arrange_labels(self):
        labels = [
            [self._label_docked, self._label_landed, self._label_supercruise,],
            [self._label_shields, self._label_silent_running, self._label_flight_assist_off],
            [self._label_hardpoints, self._label_cargo_scoop, self._label_landing_gear],
            [self._label_lights, self._label_night_vision, self._label_scooping_fuel],
            [self._label_fsd_mass_locked, self._label_fsd_charging, self._label_fsd_hyper_charging],
            [self._label_fsd_jump, self._label_fsd_cooldown, self._label_hud_analysis_mode]
        ]

        for i_row, row in enumerate(labels):
            for i_col, label in enumerate(row):
                label.configure(state='disabled')
                label.grid(column=i_col, row=i_row, padx=5, pady=5)

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
