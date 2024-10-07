# HEMA Herald

An app to run HEMA tournaments. Currently in development.

Goals:

- provide a reliable solution to run HEMA tournaments
- ease of customization for uncommon rules
- ease of installation
- free-as-in-freedom

## Getting started

### Installation

- Install Python, if you do not have it yet.
Currently, the app is tested on Python 3.11 only.
- Create a virtual environment.
- Activate your virtual environment.
- Install the app from PyPi `pip install -U hemaherald`.
- Run the app with `python -m hemaherald`


### Configuration

When started, the app searches for a config.

- path provided in `HEMAHERALD_CONFIG_PATH` environment variable
- file `hemaherald.conf` in your working directory

If the app does not find a config, it uses reasonable defaults.

Sample config:

```
[timer]
duration_sec = 150
tick_duration_sec = 0.05
```

#### Timer Section

- `duration_sec`: duration of the fight, must be a nonnegative integer
- `tick_duration_sec`: time between timer wake-ups, must be a float between 0.01 and 0.2,
0.05 is a reasonable default.
0.2 is likely to be too much, as it might allow an extra action at the end of the fight.
I'm considering to make duration of the last timer tick computed based on remaining time,
so that the fight end is really precise.
