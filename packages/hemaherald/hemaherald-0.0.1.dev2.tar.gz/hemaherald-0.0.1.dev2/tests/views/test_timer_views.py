import pytest


from hemaherald.views.timer import (
    format_remaining_time_seconds_precision,
    format_remaining_time_ms_precision,
)


def sec2ms(x: float | int) -> float:
    return x * 1000.0


@pytest.mark.parametrize(['ms', 'expected', 'message'], [
    (sec2ms(10 * 60 + 20), '10:20', '2-digit minutes and 2-digit seconds'),
    (sec2ms(2 * 60 + 30), '02:30', '1-digit minutes and 2-digit seconds'),
    (sec2ms(45), '00:45', '0-digit minutes and 2-digit seconds'),
    (sec2ms(60), '01:00', '60 seconds are a minute'),
    (sec2ms(61 * 60 + 20), '61:20', 'We do not show hours'),
    (sec2ms(100 * 60 + 20), '100:20', 'Yet we still do support extremely long fights'),
    (sec2ms(9), '00:09', '1-digit seconds'),
    (sec2ms(69), '01:09', '1-digit minutes and 1-digit seconds'),
    (sec2ms(0.9), '00:01', 'Fractional seconds are rounded up'),
    (sec2ms(1.01), '00:02', 'Fractional seconds are rounded UP'),
    (sec2ms(0.0), '00:00', 'Zero actually gets displayed'),
])
def test_format_remaining_time_seconds_precision(ms, expected, message):
    assert format_remaining_time_seconds_precision(ms) == expected, message


@pytest.mark.parametrize(['ms', 'expected', 'message'], [
    (sec2ms(10 * 60 + 20), '10:20.000', '2-digit minutes and 2-digit seconds'),
    (sec2ms(2 * 60 + 30), '02:30.000', '1-digit minutes and 2-digit seconds'),
    (sec2ms(45), '00:45.000', '0-digit minutes and 2-digit seconds'),
    (sec2ms(60), '01:00.000', '60 seconds are a minute'),
    (sec2ms(61 * 60 + 20), '61:20.000', 'We do not show hours'),
    (sec2ms(100 * 60 + 20), '100:20.000', 'Yet we still do support extremely long fights'),
    (sec2ms(9), '00:09.000', '1-digit seconds'),
    (sec2ms(69), '01:09.000', '1-digit minutes and 1-digit seconds'),
    (sec2ms(0.9), '00:00.900', 'Display milliseconds for fractional seconds'),
    (sec2ms(1.123), '00:01.123', '1-digit seconds, 3-digit ms'),
    (sec2ms(1.001), '00:01.001', '1-digit seconds, 1-digit ms'),
    (sec2ms(1.001234), '00:01.002', 'Fractional milliseconds are rounded up'),
    (sec2ms(0.0), '00:00.000', 'Zero actually gets displayed'),
])
def test_format_remaining_time_ms_precision(ms, expected, message):
    assert format_remaining_time_ms_precision(ms) == expected, message



