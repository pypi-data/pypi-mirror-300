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

import tkinter as tk

from hemaherald.models.timer import (
    TIMER_STARTED_EVENT,
    TIMER_STOPPED_EVENT,
    TIMER_UPDATED_EVENT,
    TimerModel,
)
from hemaherald.views.timer import (
    SimpleTimerView,
    TimerControlsOperations,
    SecretaryTimerView,
)


class SimpleTimerController:
    def __init__(self, root: tk.Misc, timer_model: TimerModel, timer_view: SimpleTimerView) -> None:
        self._root = root
        self._model: TimerModel = timer_model
        self._view: SimpleTimerView = timer_view
        self._root.bind(TIMER_UPDATED_EVENT, self._process_timer_update_event, add=True)

    def _process_timer_update_event(self, event: tk.Event) -> None:
        ms = self._model.get_remaining_ms()
        self._view.update_value(ms)


class TimerController:
    def __init__(self, root: tk.Misc, timer_model: TimerModel, timer_view: SecretaryTimerView) -> None:
        self._root = root
        self._timer = timer_model
        self._view = timer_view
        self._root.bind(TIMER_STARTED_EVENT, self._process_timer_start_event, add=True)
        self._root.bind(TIMER_STOPPED_EVENT, self._process_timer_stop_event, add=True)
        self._bind_events()
        self._view.sync_total_time(self._timer.get_duration_sec())

    def _bind_events(self):
        self._view.bind_command(TimerControlsOperations.START_PAUSE, self.start_pause)
        self._view.bind_command(TimerControlsOperations.RESET, self.reset)
        self._view.bind_command(TimerControlsOperations.RECONFIGURE, self.reconfigure)
        self._view.bind_command(TimerControlsOperations.ADD_TIME, self.add_time)
        self._view.bind_command(TimerControlsOperations.REMOVE_TIME, self.remove_time)

    def start_pause(self) -> None:
        if self._timer.is_running():
            self._timer.stop()
        else:
            self._timer.start()

    def reset(self) -> None:
        if not self._timer.is_running():
            self._timer.reset()

    def _change_time(self, increase: bool):
        delta = self._view.get_delta()
        self._timer.change_time(delta if increase else -delta)

    def add_time(self) -> None:
        self._change_time(increase=True)

    def remove_time(self) -> None:
        self._change_time(increase=False)

    def reconfigure(self) -> None:
        if self._timer.is_running():
            return
        self._timer.reconfigure(self._view.get_new_total_time())
        self._view.sync_total_time(self._timer.get_duration_sec())

    def _process_timer_start_event(self, event: tk.Event) -> None:
        self._view.sync_with_timer_running_state(True)

    def _process_timer_stop_event(self, event: tk.Event) -> None:
        self._view.sync_with_timer_running_state(False)
