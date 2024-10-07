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
import re
import tkinter as tk
import tkinter.ttk as ttk
import typing as tp

from enum import Enum
from functools import partial


def format_remaining_time_seconds_precision(total_ms: float) -> str:
    """
    Formats remaining time to show it to fighters and judges

    Number of minutes is shown as an integer, left-padded to two digits
    with zeros. Seconds are always shown as two digits. Fractional
    seconds are rounded up to nearest integer, so that we do not
    display "00:00" when there is 0.49 seconds remaining.

    :param total_ms: remaining time, in milliseconds
    :return: string representation
    """
    remaining_sec = int(math.ceil(total_ms / 1000))
    minutes, seconds = divmod(remaining_sec, 60)
    return f'{minutes:02}:{seconds:02}'


def format_remaining_time_ms_precision(total_ms: float) -> str:
    """
    Formats remaining time to show it to the secretary

    The secretary needs immediate feedback that he/she started the
    timer, so we display milliseconds here.

    Number of minutes is shown as an integer, left-padded to two digits
    with zeros. Seconds are always shown as two digits. Milliseconds
    are always shown as three digits. Fractional milliseconds are
    rounded up to nearest integer, so that we do not show an extremely
    long number. Direction of rounding is not really important, but is
    chosen to be up for consistency with the other display.

    :param total_ms: remaining time, in milliseconds
    :return: string representation
    """
    remaining_sec = int(math.floor(total_ms / 1000))
    minutes, seconds = divmod(remaining_sec, 60)
    ms = math.ceil(total_ms % 1000)
    return f'{minutes:02}:{seconds:02}.{ms:03}'


class SimpleTimerView:
    def __init__(self, root: tk.Misc, formatter: tp.Callable[[float], str]) -> None:
        self._root = root
        self._formatter = formatter
        self._variable = tk.StringVar(self._root, self._formatter(0))
        self.label = ttk.Label(self._root, textvariable=self._variable)

    def update_value(self, ms: float) -> None:
        self._variable.set(self._formatter(ms))

    def pack(self):
        self.label.pack()
        self.label.configure()


class TimerControlsOperations(Enum):
    START_PAUSE = 0
    RESET = 1
    RECONFIGURE = 2
    ADD_TIME = 3
    REMOVE_TIME = 4


class TimerInputValueError(Exception):
    pass


class SecretaryTimerView:
    def __init__(self, root: tk.Misc):
        self._root = root
        self._frame = ttk.Frame(self._root)

        self._regex_nonnegative_integer_validation = re.compile(r'(^[1-9]\d*$)|(^0$)')

        int_validation_command_name = self._frame.register(self._validate_nonnegative_integer)

        # Frame for start/pause & reset controls
        self._frame_primary_controls = ttk.Frame(self._frame)
        self._var_start_pause = tk.StringVar(self._frame_primary_controls, value='Start')
        self._button_start_pause = ttk.Button(self._frame_primary_controls, textvariable=self._var_start_pause)
        self._button_reset = ttk.Button(self._frame_primary_controls, text='Reset')

        self._frame_time_change = ttk.Frame(self._frame)
        self._label_time = ttk.Label(self._frame_time_change, text='Change remaining time (sec)')
        self._button_add_time = ttk.Button(self._frame_time_change, text='+')
        self._button_remove_time = ttk.Button(self._frame_time_change, text='-')
        self._var_time_change = tk.StringVar(self._frame_time_change, value='1')
        invalid_change_time_command_name = self._frame.register(
            partial(self._fix_nonnegative_integer_input, var=self._var_time_change))
        self._entry_time = ttk.Entry(self._frame_time_change,
                                     textvariable=self._var_time_change,
                                     validatecommand=(int_validation_command_name, '%P'),
                                     validate='all',
                                     invalidcommand=(invalid_change_time_command_name, '%P'))

        self._frame_configuration = ttk.Frame(self._frame)
        self._label_new_total_time = ttk.Label(self._frame_configuration, text='Total time, sec')
        self._var_new_total_time = tk.StringVar(self._frame_configuration, value='0')
        invalid_total_time_command_name = self._frame.register(
            partial(self._fix_nonnegative_integer_input, var=self._var_new_total_time)
        )
        self._entry_new_total_time = ttk.Entry(self._frame_configuration,
                                               textvariable=self._var_new_total_time,
                                               validatecommand=(int_validation_command_name, '%P'),
                                               validate='all',
                                               invalidcommand=(invalid_total_time_command_name, '%P'))
        self._label_current_total_time = ttk.Label(self._frame_configuration, text='Current total time, sec')
        self._var_current_total_time = tk.IntVar(self._frame_configuration)
        self._label_current_total_time_value = ttk.Label(self._frame_configuration,
                                                         textvariable=self._var_current_total_time)
        self._button_reconfigure = ttk.Button(self._frame_configuration, text='Reconfigure')

        self._operations_mapping = {
            TimerControlsOperations.START_PAUSE.value: self._button_start_pause,
            TimerControlsOperations.RESET.value: self._button_reset,
            TimerControlsOperations.ADD_TIME.value: self._button_add_time,
            TimerControlsOperations.REMOVE_TIME.value: self._button_remove_time,
            TimerControlsOperations.RECONFIGURE.value: self._button_reconfigure,
        }

    def _validate_nonnegative_integer(self, new_value: str) -> bool:
        match = self._regex_nonnegative_integer_validation.match(new_value)
        if not match:
            return False
        return True

    def _fix_nonnegative_integer_input(self, new_value: str, var: tk.StringVar) -> None:
        if new_value == '':
            var.set('0')
            return
        result = new_value
        if re.match(r'^-\d+', result):
            result = re.sub('^-', '', result)
        if new_value.startswith('0') and len(new_value) > 1:
            result = re.sub('^0+', '', result)
        if self._validate_nonnegative_integer(result):
            var.set(result)

    def _fix_time_change_empty_input(self, new_value) -> None:
        if new_value == '':
            self._var_time_change.set('0')

    def _fix_new_total_time_empty_input(self, new_value) -> None:
        if new_value == '':
            self._var_new_total_time.set('0')

    def bind_command(self, operation: TimerControlsOperations, command: tp.Callable[..., None]):
        self._operations_mapping[operation.value].configure(command=command)

    def sync_with_timer_running_state(self, is_running: bool) -> None:
        self._var_start_pause.set('Pause' if is_running else 'Start')
        self._button_reset.configure(state=tk.DISABLED if is_running else tk.NORMAL)
        self._button_reconfigure.configure(state=tk.DISABLED if is_running else tk.NORMAL)

    def get_delta(self) -> int:
        raw_value = self._var_time_change.get()
        if not self._validate_nonnegative_integer(raw_value):
            raise TimerInputValueError()
        value = int(raw_value)
        return value

    def get_new_total_time(self) -> int:  # TODO: refactor to extract reusable part
        raw_value = self._var_new_total_time.get()
        if not self._validate_nonnegative_integer(raw_value):
            raise TimerInputValueError()
        value = int(raw_value)
        return value

    def sync_total_time(self, seconds: int) -> None:
        self._var_new_total_time.set(str(seconds))
        self._var_current_total_time.set(seconds)

    def pack(self) -> None:
        # TODO: make it proper
        self._frame_primary_controls.pack(padx=5, pady=5)
        # self._frame_primary_controls.configure(borderwidth=2, relief=tk.RIDGE)
        self._button_reset.grid(row=0, column=0, padx=5, pady=5)
        self._button_start_pause.grid(row=0, column=1, padx=5, pady=5)

        self._frame_time_change.pack(padx=5, pady=5)
        self._label_time.grid(row=0, column=0, rowspan=1, columnspan=3)
        self._button_add_time.grid(row=1, column=0, padx=5, pady=5)
        self._button_add_time.configure(width=3)
        self._entry_time.grid(row=1, column=1, padx=5, pady=5)
        self._entry_time.configure(justify='right')
        self._button_remove_time.grid(row=1, column=2, padx=5, pady=5)
        self._button_remove_time.configure(width=3)
        self._frame_time_change.grid_columnconfigure(0, weight=0)
        self._frame_time_change.grid_columnconfigure(1, weight=1)
        self._frame_time_change.grid_columnconfigure(2, weight=0)

        self._frame_configuration.pack()
        self._label_new_total_time.grid(row=0, column=0, padx=5, pady=2, sticky='W')
        self._label_current_total_time.configure(justify='left')
        self._entry_new_total_time.grid(row=0, column=1, padx=5, pady=2, sticky='E')
        self._entry_new_total_time.configure(justify='right', width=6)
        self._label_current_total_time.grid(row=1, column=0, padx=5, pady=2, sticky='W')
        self._label_current_total_time.configure(justify='left')
        self._label_current_total_time_value.grid(row=1, column=1, padx=5, pady=2, sticky='E')
        self._label_current_total_time_value.configure(justify='right')
        self._button_reconfigure.grid(row=2, column=0, rowspan=1, columnspan=2, padx=5, pady=5)

        self._frame.pack()  # fill='x', expand=True
