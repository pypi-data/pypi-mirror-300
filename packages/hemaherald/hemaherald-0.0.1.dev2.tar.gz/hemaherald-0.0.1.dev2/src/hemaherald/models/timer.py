# HEMA Herald (hemaherald), an app for running HEMA tournaments
# Copyright (C) 2024 Danila Shershukov
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import math
import time
import tkinter as tk


TIMER_UPDATED_EVENT = '<<TimerUpdated>>'
TIMER_STARTED_EVENT = '<<TimerStarted>>'
TIMER_STOPPED_EVENT = '<<TimerStopped>>'


class TimerError(Exception):
    pass


class TimerConfigurationError(TimerError):
    """
    Raised if timer is configured incorrectly
    """
    pass


class TimerIsRunningError(TimerError):
    """
    Raised on attempt to call a method which can be executed only when
    the timer is stopped
    """
    pass


class TimerModel:
    """
    Timer that works with Tkinter event loop

    Internally, it relies on `time.monotonic` to track time, so
    system clock changes due to ntp syncs or manual changes will not
    affect it.

    The other thing the timer relies on is the Tkinter event loop to
    wake it up several times per second to check if time has run out
    and to emit events to update the interface. As the Tkinter event
    loop is single-threaded, make sure that no other event occupies
    the main process for too long.

    Timer wake-ups do not have to be too frequent. About 1/20 second
    of sleep time is OK.

    Events that the timer can fire:

    - `TIMER_UPDATED_EVENT` to indicate that the number of remaining
      milliseconds should be synced
    - `TIMER_STARTED_EVENT` when timer is started
    - `TIMER_STOPPED_EVENT` when timer is stopped
    """
    def __init__(self, root: tk.Misc, duration_sec: int, tick_duration_sec: float = 0.05):
        """
        Creates the timer

        :param root: widget to bind to
        :param duration_sec: duration, seconds >0
        :param tick_duration_sec: how long a single timer tick takes,
          default is 0.05 seconds
        """
        self._validate_inputs(duration_sec, tick_duration_sec)

        self._root: tk.Misc = root
        self._duration_sec: int = duration_sec
        self._step_ms: float = tick_duration_sec * 1000
        self._remaining_ms: float = float(duration_sec * 1000)
        self._is_running: bool = False
        self._previous_tick: float = time.monotonic()

    @staticmethod
    def _validate_inputs(duration_sec: int, tick_duration_sec: float) -> None:
        if not isinstance(duration_sec, int) or duration_sec < 0:
            raise TimerConfigurationError('Timer duration must be a nonnegative integer', duration_sec)
        if not isinstance(tick_duration_sec, float) or tick_duration_sec < 0.01 or tick_duration_sec > 0.2:
            raise TimerConfigurationError('Timer tick duration must be a float 0.01 <= x <= 0.2', tick_duration_sec)

    def is_running(self) -> bool:
        """
        Current state of the timer

        :return: `True` if it is running, `False` otherwise
        """
        return self._is_running

    def get_remaining_ms(self) -> float:
        """
        Time until the end, in milliseconds

        :return: time until the end, in milliseconds
        """
        return self._remaining_ms

    def get_tick_duration_ms(self) -> float:
        """
        Timer tick duration, in milliseconds
        
        :return: timer tick duration, in milliseconds
        """
        return self._step_ms

    def get_duration_sec(self) -> int:
        """
        Timer duration, in seconds

        :return: timer duration, in seconds
        """
        return self._duration_sec

    def _notify(self) -> None:
        self._root.event_generate(TIMER_UPDATED_EVENT)

    def _set_state(self, is_running: bool) -> None:
        self._is_running = is_running
        if is_running:
            self._root.event_generate(TIMER_STARTED_EVENT)
        else:
            self._root.event_generate(TIMER_STOPPED_EVENT)

    def _tick(self) -> None:
        if not self._is_running:
            # Do not raise errors as the event could be scheduled
            # before the timer was stopped.
            return

        current_time = time.monotonic()
        elapsed_ms = (current_time - self._previous_tick) * 1000  # time.monotonic returns seconds
        remaining_ms = max(self._remaining_ms - elapsed_ms, 0.0)
        self._remaining_ms = remaining_ms
        self._previous_tick = current_time

        self._notify()
        if math.isclose(remaining_ms, 0):
            self._stop()
            return
        self._root.after(int(self._step_ms), self._tick)  # `after` expects integer ms

    def _stop(self) -> None:
        self._set_state(False)

    def start(self) -> None:
        """
        Starts the timer
        
        `TIMER_UPDATED_EVENT` and `TIMER_STOPPED_EVENT` are fired
        and the next tick is scheduled.
        
        
        If timer is already running, it does nothing.
        
        :return: 
        """
        if self._is_running:
            raise TimerIsRunningError()

        self._notify()
        self._set_state(True)
        self._previous_tick = time.monotonic()
        self._root.after(int(self._step_ms), self._tick)  # `after` expects integer ms

    def stop(self) -> None:
        """
        Stops the timer

        `TIMER_UPDATED_EVENT` and `TIMER_STOPPED_EVENT` are fired

        :return: None
        """
        self._notify()
        self._stop()

    def reset(self) -> None:
        if self._is_running:
            raise TimerIsRunningError()

        self._remaining_ms = self._duration_sec * 1000
        self._notify()

    def change_time(self, delta_sec: int) -> None:
        if not isinstance(delta_sec, int):
            raise TimerConfigurationError('Change in remaining time must be an integer', delta_sec)

        new_time = max(self._remaining_ms + delta_sec * 1000, 0)
        self._remaining_ms = new_time
        self._notify()

    def reconfigure(self, duration_sec, resolution_sec: float = 0.05) -> None:
        if self._is_running:
            raise TimerIsRunningError()

        self._validate_inputs(duration_sec, resolution_sec)
        self._duration_sec = duration_sec
        self._step_ms = resolution_sec * 1000
