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

import configparser
import os
import pathlib
import typing as tp

from dataclasses import dataclass

DEFAULT_CONFIG_NAME = 'hemaherald.conf'


def locate_config() -> tp.Optional[pathlib.Path]:
    environment_path = os.environ.get('HEMAHERALD_CONFIG_PATH', None)
    if environment_path:
        path = pathlib.Path(environment_path)
        if path.exists() and path.is_file():
            return path

    working_directory = pathlib.Path(os.getcwd())
    config_path = working_directory / DEFAULT_CONFIG_NAME
    if not config_path.exists():
        return None
    return config_path


def read_config(path: pathlib.Path) -> str:
    with open(path) as f:
        return f.read()


@dataclass
class TimerConfig:
    duration_sec: int = 60
    step_duration_sec: float = 0.05


@dataclass
class AppConfig:
    timer_config: TimerConfig


def parse_config(text: str):
    parser = configparser.ConfigParser()
    parser.read_string(text)
    timer_duration_sec = parser.getint('timer', 'duration_sec')
    timer_step_duration_sec = parser.getfloat('timer', 'tick_duration_sec')

    timer_config = TimerConfig(timer_duration_sec, timer_step_duration_sec)
    app_config = AppConfig(timer_config)
    return app_config


def configure() -> AppConfig:
    path = locate_config()
    if not path:
        return AppConfig(TimerConfig())

    config_text = read_config(path)
    app_config = parse_config(config_text)
    return app_config
