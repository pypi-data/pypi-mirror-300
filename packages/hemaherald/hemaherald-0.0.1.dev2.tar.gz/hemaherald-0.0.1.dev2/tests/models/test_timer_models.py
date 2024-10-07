import time
import tkinter as tk

import pytest
from pytest_mock.plugin import MockerFixture

from hemaherald.models.timer import (
    TimerModel,
    TIMER_STARTED_EVENT,
    TIMER_UPDATED_EVENT,
    TIMER_STOPPED_EVENT,
    TimerConfigurationError,
    TimerIsRunningError,
)


##################
# __init__ tests #
##################

@pytest.mark.parametrize(['duration_sec', 'expected', 'message'], [
    (90, 90, 'Simple case for duration'),
    (0, 0, 'Allow creating timer with zero duration'),
    (3600 * 24, 3600 * 24, 'Allow really long duration'),
])
def test_timer_init__allowed_duration(duration_sec, expected, message):
    root = tk.Tk()
    timer = TimerModel(root, duration_sec)
    assert timer.get_duration_sec() == expected, message


@pytest.mark.parametrize(['bad_duration_value', 'message'], [
    (-1, 'Negative timer duration just makes no sense'),
    (60.1, 'Total fight duration in fractional seconds is too precise for practical purposes'),
    (60.0, 'Do not accept floats'),
])
def test_timer_init__fails_on_bad_duration(bad_duration_value, message):
    root = tk.Tk()
    with pytest.raises(TimerConfigurationError, match=r'Timer duration.*'):
        TimerModel(root, bad_duration_value)


def test_timer_init__has_reasonable_default_tick_duration():
    root = tk.Tk()
    timer = TimerModel(root, 60)
    assert timer.get_tick_duration_ms() == 50


@pytest.mark.parametrize(['tick_duration_sec', 'expected', 'message'], [
    (0.06, 60, 'Some common tick duration'),
    (0.01, 10, '10 ms per tick is still allowed'),
    (0.2, 200, '200 ms per tick is still allowed'),
    (0.0301, 30.1, 'Internally, no truncation to milliseconds happens'),
    (0.0309, 30.9, 'Internally, no truncation to milliseconds happens'),
])
def test_timer_init__allowed_tick_duration(tick_duration_sec, expected, message):
    root = tk.Tk()
    timer = TimerModel(root, 60, tick_duration_sec)
    assert timer.get_tick_duration_ms() == pytest.approx(expected), message


@pytest.mark.parametrize(['tick_duration_sec', 'message'], [
    ('', 'Bad type'),
    (0.0, 'Definitely do not allow zero tick duration'),
    (0.0099999, 'Anything below 0.01 is considered too frequent'),
    (0.2000001, 'Anything above 0.2 is considered too rare'),
])
def test_timer_init__fails_on_bad_tick_duration(tick_duration_sec, message):
    root = tk.Tk()
    with pytest.raises(TimerConfigurationError, match=r'Timer tick duration.*'):
        TimerModel(root, 60, tick_duration_sec)


def test_timer_init__timer_is_not_started_on_creation():
    root = tk.Tk()
    timer = TimerModel(root, 60)
    assert timer.is_running() is False


################
# Test start() #
################

@pytest.fixture
def prepare_timer_60__0_05(mocker: MockerFixture):
    root = tk.Tk()
    mock_event_generate = mocker.patch.object(root, 'event_generate', autospec=True)
    mock_after = mocker.patch.object(root, 'after', autospec=True)
    timer = TimerModel(root, 60, 0.05)

    return timer, mock_event_generate, mock_after


def test_timer_start__main_case(mocker: MockerFixture, prepare_timer_60__0_05):
    """
    Testing normal timer behaviour on start
    """
    # Get mock objects
    timer, mock_event_generate, mock_after = prepare_timer_60__0_05

    tick_duration = timer.get_tick_duration_ms()
    t_creation = timer._previous_tick
    time.sleep(0.01)

    # Payload
    timer.start()

    # Test
    mock_event_generate.assert_has_calls(calls=[mocker.call(TIMER_UPDATED_EVENT), mocker.call(TIMER_STARTED_EVENT)])
    mock_after.assert_called_once_with(tick_duration, timer._tick)
    assert timer._previous_tick > t_creation, 'Measuring time from start, not creation'
    assert timer.is_running() is True, 'Must have set state to running'


def test_timer_start__already_running_case(prepare_timer_60__0_05):
    timer, _, _ = prepare_timer_60__0_05
    timer.start()
    with pytest.raises(TimerIsRunningError):
        timer.start()


###############
# Test stop() #
###############

def test_timer_stop__main_case(mocker: MockerFixture, prepare_timer_60__0_05):
    # Prepare mock objects
    timer, mock_event_generate, mock_after = prepare_timer_60__0_05

    # Prepare timer state
    timer.start()
    start_time = timer._remaining_ms
    time.sleep(0.01)

    # Reset mocks
    mock_event_generate.reset_mock()
    mock_after.reset_mock()

    # Payload
    timer.stop()

    # Test
    mock_event_generate.assert_has_calls([mocker.call(TIMER_STOPPED_EVENT)])
    mock_after.assert_not_called()
    assert timer.is_running() is False, 'State must reflect that timer is stopped'
    assert timer._remaining_ms == pytest.approx(start_time), 'Stopping the timer does not change remaining time'


def test_timer_stop__can_stop_twice(prepare_timer_60__0_05):
    # Prepare mock objects
    timer, _, _ = prepare_timer_60__0_05
    timer.start()
    timer.stop()

    # Payload
    timer.stop()  # Must not raise anything


####################
# Test reconfigure #
####################

@pytest.mark.parametrize(['duration_sec', 'expected', 'message'], [
    (90, 90, 'Simple case for duration change'),
    (0, 0, 'Allow changing duration to zero'),
    (3600 * 24, 3600 * 24, 'Allow really long duration'),
])
def test_timer_reconfigure__allowed_duration(prepare_timer_60__0_05, duration_sec, expected, message):
    timer, _, _ = prepare_timer_60__0_05
    timer.reconfigure(duration_sec)
    assert timer.get_duration_sec() == expected, message


@pytest.mark.parametrize(['bad_duration_value', 'message'], [
    (-1, 'Negative timer duration just makes no sense'),
    (60.1, 'Total fight duration in fractional seconds is too precise for practical purposes'),
    (60.0, 'Do not accept floats'),
])
def test_timer_reconfigure__fails_on_bad_duration(prepare_timer_60__0_05, bad_duration_value, message):
    timer, _, _ = prepare_timer_60__0_05
    with pytest.raises(TimerConfigurationError, match=r'Timer duration.*'):
        timer.reconfigure(bad_duration_value)


@pytest.mark.parametrize(['tick_duration_sec', 'expected', 'message'], [
    (0.06, 60, 'Some common tick duration'),
    (0.01, 10, '10 ms per tick is still allowed'),
    (0.2, 200, '200 ms per tick is still allowed'),
    (0.0301, 30.1, 'Internally, no truncation to milliseconds happens'),
    (0.0309, 30.9, 'Internally, no truncation to milliseconds happens'),
])
def test_timer_reconfigure__allowed_tick_duration(prepare_timer_60__0_05, tick_duration_sec, expected, message):
    timer, _, _ = prepare_timer_60__0_05
    timer.reconfigure(60, tick_duration_sec)
    assert timer.get_tick_duration_ms() == pytest.approx(expected), message


@pytest.mark.parametrize(['tick_duration_sec', 'message'], [
    ('', 'Bad type'),
    (0.0, 'Definitely do not allow zero tick duration'),
    (0.0099999, 'Anything below 0.01 is considered too frequent'),
    (0.2000001, 'Anything above 0.2 is considered too rare'),
])
def test_timer_reconfigure__fails_on_bad_tick_duration(prepare_timer_60__0_05, tick_duration_sec, message):
    timer, _, _ = prepare_timer_60__0_05
    with pytest.raises(TimerConfigurationError, match=r'Timer tick duration.*'):
        timer.reconfigure(60, tick_duration_sec)


def test_timer_reconfigure__has_reasonable_default_tick_duration(prepare_timer_60__0_05):
    timer, _, _ = prepare_timer_60__0_05
    timer.reconfigure(60, 0.04)

    timer.reconfigure(60)
    assert timer.get_tick_duration_ms() == 50


def test_timer_reconfigure__does_not_change_remaining_time(prepare_timer_60__0_05):
    timer, _, _ = prepare_timer_60__0_05

    initial_time = timer._remaining_ms
    timer.reconfigure(90, 0.04)
    new_time = timer._remaining_ms
    assert new_time == pytest.approx(initial_time)


def test_timer_reconfigure__does_not_work_when_timer_is_running(prepare_timer_60__0_05):
    timer, _, _ = prepare_timer_60__0_05
    timer.start()
    with pytest.raises(TimerIsRunningError):
        timer.reconfigure(90)


def test_timer_reconfigure__does_not_launch_timer(prepare_timer_60__0_05):
    timer, _, _ = prepare_timer_60__0_05
    timer.reconfigure(90)
    assert timer.is_running() is False


####################
# Test change_time #
####################

@pytest.mark.parametrize(['base_sec', 'delta_sec', 'expected_ms', 'message'], [
    (45, 5, 50 * 1000.0, 'Common added time'),
    (45, -5, 40 * 1000.0, 'Common subtracted time'),
    (45, -45, 0.0, 'Subtracting to zero is allowed'),
    (45, -50, 0.0, 'If resulting value turns out to be less than zero, truncate'),
    (45, 0, 45 * 1000.0, 'Zero is pointless, but still allowed')
])
def test_timer_change_time__valid_inputs(prepare_timer_60__0_05, base_sec, delta_sec, expected_ms, message):
    timer, _, _ = prepare_timer_60__0_05
    timer.reconfigure(base_sec)
    timer.reset()
    timer.change_time(delta_sec)
    assert timer.get_remaining_ms() == pytest.approx(expected_ms)


@pytest.mark.parametrize(['value', 'message'], [
    (1.0, 'Floats are not allowed'),
])
def test_timer_change_time__invalid_inputs(prepare_timer_60__0_05, value, message):
    timer, _, _ = prepare_timer_60__0_05
    with pytest.raises(TimerConfigurationError, match=r'Change in remaining time.*'):
        timer.change_time(value)


def test_timer_change_time__works_in_running_state(prepare_timer_60__0_05):
    timer, _, _ = prepare_timer_60__0_05
    timer.start()
    timer.change_time(30)
    assert timer.get_remaining_ms() == pytest.approx(90.0 * 1000)


def test_timer_change_time__does_not_change_state(prepare_timer_60__0_05):
    timer, _, _ = prepare_timer_60__0_05
    timer.start()
    timer.change_time(5)
    state_after_change_for_running = timer.is_running()
    timer.stop()
    timer.change_time(5)
    state_after_change_for_stopped = timer.is_running()
    assert state_after_change_for_running is True
    assert state_after_change_for_stopped is False


def test_timer_change_time__triggers_ui_change(prepare_timer_60__0_05):
    timer, mock_event_generate, mock_after = prepare_timer_60__0_05
    timer.change_time(5)
    mock_event_generate.assert_called_once_with(TIMER_UPDATED_EVENT)


def test_timer_change_time__does_not_reschedule(prepare_timer_60__0_05):
    timer, mock_event_generate, mock_after = prepare_timer_60__0_05
    timer.change_time(5)
    mock_after.assert_not_called()


##############
# Test reset #
##############

@pytest.mark.parametrize(['change', 'message'], [
    (-5, 'Reset works when remaining time is less than duration'),
    (0, 'Reset works when remaining time is equal to duration'),
    (5, 'Reset works when remaining time is greater than duration'),
    (-60, 'Reset works when remaining time is zero'),
])
def test_timer_reset__resets_time(prepare_timer_60__0_05, change, message):
    timer, _, _ = prepare_timer_60__0_05
    timer.change_time(change)
    timer.reset()
    assert timer.get_remaining_ms() == pytest.approx(60 * 1000.0)


def test_timer_reset__sends_sync_event(prepare_timer_60__0_05):
    timer, mock_event_generate, mock_after = prepare_timer_60__0_05
    timer.reset()

    mock_event_generate.assert_called_once_with(TIMER_UPDATED_EVENT)
    mock_after.assert_not_called()


def test_timer_reset__does_not_work_when_timer_is_running(prepare_timer_60__0_05):
    timer, _, _ = prepare_timer_60__0_05
    timer.start()
    with pytest.raises(TimerIsRunningError):
        timer.reset()


def test_timer_reset__does_not_change_state(prepare_timer_60__0_05):
    timer, _, _ = prepare_timer_60__0_05
    timer.reset()
    assert timer.is_running() is False


##############
# Test _tick #
##############

def test_timer_tick__when_a_lot_of_time_remains(prepare_timer_60__0_05):
    timer, mock_event_generate, mock_after = prepare_timer_60__0_05
    timer.start()
    ms_before = timer.get_remaining_ms()
    ts_before = timer._previous_tick
    mock_event_generate.reset_mock()
    mock_after.reset_mock()

    # Imitate TK waiting for the desired time and then fire the event
    time.sleep(0.05)
    timer._tick()
    ms_after = timer.get_remaining_ms()
    ts_after = timer._previous_tick

    assert timer.is_running() is True, 'Timer must still be running'
    assert ms_before - ms_after == pytest.approx(50.0, 0.05), 'Reflected passed time is close to real'
    assert ts_after - ts_before == pytest.approx(0.05, 0.05), 'Wait time is close to real'
    mock_event_generate.assert_called_once_with(TIMER_UPDATED_EVENT)
    mock_after.assert_called_once_with(50, timer._tick)


def test_timer_tick__when_it_must_be_last(mocker: MockerFixture, prepare_timer_60__0_05):
    timer, mock_event_generate, mock_after = prepare_timer_60__0_05

    # Mess with the state, so we don't have to run the test too long
    timer._remaining_ms = 10

    timer.start()
    ms_before = timer.get_remaining_ms()
    ts_before = timer._previous_tick
    mock_event_generate.reset_mock()
    mock_after.reset_mock()

    time.sleep(0.05)
    timer._tick()
    ms_after = timer.get_remaining_ms()
    ts_after = timer._previous_tick

    assert timer.is_running() is False, 'Timer must have stopped'
    assert ms_before - ms_after == pytest.approx(10.0, 0.05), 'Timer time is close to 10 ms'
    assert ts_after - ts_before == pytest.approx(0.05, 0.05), 'Wait time is close to real'
    mock_event_generate.assert_has_calls([mocker.call(TIMER_UPDATED_EVENT), mocker.call(TIMER_STOPPED_EVENT)])
    mock_after.assert_not_called()
    assert timer.get_remaining_ms() == pytest.approx(0.0), 'Remaining time must be zero'


def test_timer_tick__is_aborted_when_timer_is_stopped(prepare_timer_60__0_05):
    timer, mock_event_generate, mock_after = prepare_timer_60__0_05

    ms_before = timer.get_remaining_ms()
    ts_before = timer._previous_tick
    mock_event_generate.reset_mock()
    mock_after.reset_mock()

    time.sleep(0.05)
    timer._tick()
    ms_after = timer.get_remaining_ms()
    ts_after = timer._previous_tick

    assert ms_before - ms_after == pytest.approx(0.0)
    assert ts_before - ts_after == pytest.approx(0.0)
    mock_event_generate.assert_not_called()
    mock_after.assert_not_called()
    assert timer.is_running() is False


# TODO: consider marking as slow
def test_timer_tick__complete_run(mocker: MockerFixture):
    root = tk.Tk()
    mock_event_generate = mocker.patch.object(root, 'event_generate', autospec=True)
    mock_after = mocker.patch.object(root, 'after', autospec=True)
    timer = TimerModel(root, 1, 0.01)

    start_time = time.monotonic()
    timer.start()
    while timer.is_running() and time.monotonic() - start_time < 2.0:
        time.sleep(0.01)
        timer._tick()
    end_time = time.monotonic()
    assert end_time - start_time == pytest.approx(1.0, abs=0.015)
