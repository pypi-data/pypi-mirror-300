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

from hemaherald.controllers.timer import TimerController, SimpleTimerController
from hemaherald.models.timer import TimerModel
from hemaherald.utils.config import configure, AppConfig
from hemaherald.views.timer import (
    SecretaryTimerView,
    SimpleTimerView,
    format_remaining_time_ms_precision,
)


class App:
    def __init__(self, config: AppConfig):
        self.config = config

        self.root = tk.Tk()
        self.timer_model = TimerModel(self.root, self.config.timer_config.duration_sec,
                                      self.config.timer_config.step_duration_sec)
        self.timer_view = SimpleTimerView(self.root, format_remaining_time_ms_precision)
        self.timer_controller = SimpleTimerController(self.root, self.timer_model, self.timer_view)

        self.timer_controls_view = SecretaryTimerView(self.root)
        self.timer_controls_controller = TimerController(self.root, self.timer_model, self.timer_controls_view)

        self.root.title('HEMA Herald')
        self.timer_view.pack()
        self.timer_controls_view.pack()
        self.timer_model.reset()


def prepare_app():
    app_config = configure()
    app = App(app_config)
    return app


def run_app(app: App):
    app.root.mainloop()


def main():
    app = prepare_app()
    run_app(app)


if __name__ == '__main__':
    main()
