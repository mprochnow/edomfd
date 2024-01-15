import queue
from tkinter import *
from tkinter import ttk

import screeninfo

from edojournal import EDOStatus
from ui.status import StatusFrame

QUEUE_CHECK_TIME = 100  # ms


class AppWindow:
    def __init__(self, monitors: list[screeninfo.Monitor], status_queue: queue.Queue):
        self._monitors: list[screeninfo.Monitor] = monitors
        self._status_queue: queue.Queue = status_queue

        self._fullscreen: bool = False

        self._tk = Tk()
        self._tk.title("EDO MFD")
        self._tk.columnconfigure(0, weight=1)
        self._tk.rowconfigure(0, weight=0)
        self._tk.rowconfigure(1, weight=1)

        self._style = ttk.Style()
        self._style.configure('TFrame', background='#000000')

        self._status_frame = StatusFrame(self._tk)
        self._status_frame.grid(column=0, row=0, sticky="news")

        self._frame = ttk.Frame(self._tk)
        self._frame.grid(column=0, row=1, sticky="news")
        self._frame.columnconfigure(0, weight=1)
        self._frame.columnconfigure(1, weight=1)

        self._label_latitude = ttk.Label(self._frame, text="Latitude: -", style='Status.TLabel')
        self._label_latitude.configure(state='disabled')
        self._label_latitude.grid(column=0, row=0, padx=0, pady=0, sticky=N + E + S + W)

        self._label_heading = ttk.Label(self._frame, text="Heading: -", style='Status.TLabel')
        self._label_heading.configure(state='disabled')
        self._label_heading.grid(column=1, row=0, padx=0, pady=0, sticky=N + E + S + W)

        self._label_longitude = ttk.Label(self._frame, text="Longitude: -", style='Status.TLabel')
        self._label_longitude.configure(state='disabled')
        self._label_longitude.grid(column=0, row=1, padx=0, pady=0, sticky=N + E + S + W)

        self._label_altitude = ttk.Label(self._frame, text="Altitude: -", style='Status.TLabel')
        self._label_altitude.configure(state='disabled')
        self._label_altitude.grid(column=1, row=1, padx=0, pady=0, sticky=N + E + S + W)

        self._tk.bind('<Escape>', self._close)
        self._tk.bind('<F11>', self._toggle_fullscreen)

        self._maybe_move_to_secondary_monitor()
        self._tk.after(QUEUE_CHECK_TIME, self._update)

    def show(self):
        self._tk.mainloop()

    def destroy(self):
        self._tk.destroy()

    def _update(self):
        self._tk.after(QUEUE_CHECK_TIME, self._update)

        while not self._status_queue.empty():
            s: EDOStatus = self._status_queue.get_nowait()

            self._status_frame.update_status(s)

            self._label_latitude.configure(text="Latitude: " + f"{s.latitude if s.latitude else '-'}")
            self._label_longitude.configure(text="Longitude: " + f"{s.longitude if s.longitude else '-'}")

            if s.heading:
                heading = f"Heading: {s.heading}°"
            else:
                heading = "Heading: -"
            self._label_heading.configure(text=heading)

            if s.altitude:
                if s.altitude > 1000:
                    altitude = f"Altitude: {s.altitude // 1000}km"
                else:
                    altitude = f"Altitude: {s.altitude}m"
            else:
                altitude = "Altitude: -"
            self._label_altitude.configure(text=altitude)

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
