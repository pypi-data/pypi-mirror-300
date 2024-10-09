"""
This module contains the Device class, which handles interactions with thermostat devices,
such as fetching device status, setting configurations, and polling for changes.

Classes:
    Device: Represents a thermostat device, allowing for status retrieval, fan control,
            system mode control, and other features.
"""
# pylint: disable=logging-fstring-interpolation

import logging
import copy
import datetime
import json
import asyncio
from contextlib import suppress
from .exceptions import SomeComfortError, APIError
from .event_emitter import EventEmitter

_LOGGER = logging.getLogger(__name__)

FAN_MODES = ['auto', 'on', 'circulate', 'follow schedule']
SYSTEM_MODES = ['emheat', 'heat', 'off', 'cool', 'auto']
HOLD_TYPES = ['schedule', 'temporary', 'permanent']
EQUIPMENT_OUTPUT_STATUS = ['off/fan', 'heat', 'cool']


def _hold_quarter_hours(deadline):
    """
    Converts a deadline time into quarter hours.

    Args:
        deadline (datetime.time): The time that must be aligned to 15-minute intervals.

    Raises:
        SomeComfortError: If the time is not on a 15-minute boundary.

    Returns:
        int: The number of quarter hours past midnight.
    """
    if deadline.minute not in (0, 15, 30, 45):
        raise SomeComfortError('Invalid time: must be on a 15-minute boundary')
    return int(((deadline.hour * 60) + deadline.minute) / 15)


def _hold_deadline(quarter_hours):
    """
    Converts quarter hours into a time.

    Args:
        quarter_hours (int): Number of quarter hours.

    Returns:
        datetime.time: The time corresponding to the given quarter hours.
    """
    minutes = quarter_hours * 15
    return datetime.time(hour=int(minutes / 60), minute=minutes % 60)


class Device:
    """
    Represents a thermostat device and provides methods to interact with the device,
    retrieve its status, and update settings.

    Attributes:
        device_id (str): Unique ID for the device.
        name (str): The name of the device.
        _mac_id (str): The MAC address of the device.
        _session (Session): The session object for API communication.
        _data (dict): Stores the latest data retrieved from the API.
        _alive (bool): Indicates if the device is currently alive.
        _commslost (bool): Indicates if communication is lost with the device.
        _polling_task (asyncio.Task): The task responsible for polling the device for changes.
    """

    def __init__(self, session, data):
        """
        Initializes the Device instance.

        Args:
            session (Session): The session used to communicate with the API.
            data (dict): Initial data for the device.
        """
        self._session = session
        self.device_id = data["DeviceID"]
        self.name = data.get("Name", "Unknown")
        self._mac_id = data.get("MacID")
        self._raw_data = data
        self._data = {}
        self._last_refresh = 0
        self._alive = None
        self._commslost = None
        self._event_emitter = EventEmitter()
        self._polling_task = None

        _LOGGER.debug(f"Initialized Device: {self.name} (ID: {self.device_id})")
        _LOGGER.debug(f"Device Settings: {json.dumps(data, indent=2)}")

    async def __aenter__(self):
        """
        Async context manager entry method. Refreshes device data.

        Returns:
            Device: The current device instance.
        """
        await self.refresh()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Async context manager exit method. Stops polling the device.
        """
        await self.stop_polling()

    def on_change(self, listener):
        """
        Registers a listener for device changes.

        Args:
            listener (Callable): The function to call when the device changes.
        """
        self._event_emitter.on(listener)

    def off_change(self, listener):
        """
        Unregisters a listener for device changes.

        Args:
            listener (Callable): The function to remove from the change listeners.
        """
        self._event_emitter.off(listener)

    async def _poll_for_changes(self, interval=120):
        """
        Polls the device at regular intervals and triggers events when data changes.

        Args:
            interval (int): The interval in seconds between each poll.
        """
        previous_data = None
        try:
            while True:
                await self.refresh()
                current_data = copy.deepcopy(self._data)

                if previous_data is not None and current_data != previous_data:
                    _LOGGER.debug(f"Device {self.name} detected changes, emitting event")
                    await self._event_emitter.emit(current_data)
                previous_data = current_data
                next_refresh = datetime.datetime.now() + datetime.timedelta(seconds=interval)
                _LOGGER.info(f"Waiting until {next_refresh.strftime('%H:%M:%S')} for next device refresh")
                await asyncio.sleep(interval)
        except asyncio.CancelledError:
            _LOGGER.info(f"Stopped polling for device {self.name}")
            raise
        except Exception as e:
            _LOGGER.error(f"Error during polling: {e}")
            raise

    async def start_polling(self, interval=120):
        """
        Starts polling the device for changes at the specified interval.

        Args:
            interval (int): The polling interval in seconds.
        """
        if self._polling_task is None:
            self._polling_task = asyncio.create_task(self._poll_for_changes(interval))
            _LOGGER.info(f"Started polling for device {self.name}")

    async def stop_polling(self):
        """
        Stops polling the device for changes.
        """
        if self._polling_task is not None:
            self._polling_task.cancel()
            with suppress(asyncio.CancelledError):
                await self._polling_task
            self._polling_task = None
            _LOGGER.info(f"Stopped polling for device {self.name}")

    async def refresh(self):
        """
        Fetches the latest data for the device from the API and updates its internal state.
        """
        try:
            data = await self._session.get_thermostat_data(self.device_id)
            if not data['success']:
                raise APIError(f'API reported failure to query device {self.device_id}')
            self._alive = data['deviceLive']
            self._commslost = data['communicationLost']
            self._data = data['latestData']
            self._last_refresh = datetime.datetime.now().timestamp()
            _LOGGER.debug(f"Refreshed Device: {self.name} (ID: {self.device_id})")
            _LOGGER.debug(f"Current Device Data: {json.dumps(self._data, indent=2)}")
        except SomeComfortError as e:
            _LOGGER.error(f"Error refreshing device data: {e}")
            raise

    async def set_status(self, settings):
        """
        Updates the device's settings with the provided dictionary.

        Args:
            settings (dict): A dictionary of settings to apply to the device.
        """
        try:
            await self._session.set_thermostat_settings(self.device_id, settings)
            await self.refresh()  # Refresh device data after updating
        except SomeComfortError as e:
            _LOGGER.error(f"Error updating device settings: {e}")
            raise

    @property
    def mac_address(self):
        """
        Returns the MAC address of the device.

        Returns:
            str: The MAC address of the device.
        """
        return self._mac_id

    @property
    def is_alive(self):
        """
        Indicates whether the device is currently alive and connected.

        Returns:
            bool: True if the device is alive, False otherwise.
        """
        return self._alive and not self._commslost

    @property
    async def fan_running(self):
        """
        Indicates whether the fan is currently running.

        Returns:
            bool: True if the fan is running, False otherwise.
        """
        await self.refresh()
        if self._data['hasFan']:
            return self._data['fanData']['fanIsRunning']
        return False

    @property
    async def fan_mode(self):
        """
        Returns the current fan mode.

        Returns:
            str: One of FAN_MODES, indicating the current fan setting.
        """
        await self.refresh()
        try:
            return FAN_MODES[self._data['fanData']['fanMode']]
        except (KeyError, TypeError, IndexError) as exc:
            if self._data['hasFan']:
                raise APIError(f'Unknown fan mode {self._data["fanData"]["fanMode"]}') from exc
            return None

    async def set_fan_mode(self, mode):
        """
        Sets the fan mode.

        Args:
            mode (str): The fan mode to set. Must be one of FAN_MODES.
        """
        try:
            mode_index = FAN_MODES.index(mode)
        except ValueError as exc:
            raise SomeComfortError(f'Invalid fan mode `{mode}`') from exc

        key = f'fanMode{mode.title()}Allowed'
        if not self._data['fanData'][key]:
            raise SomeComfortError(f'Device does not support {mode}')
        await self.set_status({'FanMode': mode_index})

    @property
    async def system_mode(self):
        """
        Returns the current system mode.

        Returns:
            str: One of SYSTEM_MODES, indicating the current system mode.
        """
        await self.refresh()
        try:
            return SYSTEM_MODES[self._data['uiData']['SystemSwitchPosition']]
        except KeyError as exc:
            raise APIError(f'Unknown system mode {self._data["uiData"]["SystemSwitchPosition"]}') from exc 

    async def set_system_mode(self, mode):
        """
        Sets the system mode.

        Args:
            mode (str): The system mode to set. Must be one of SYSTEM_MODES.
        """
        try:
            mode_index = SYSTEM_MODES.index(mode)
        except ValueError as exc:
            raise SomeComfortError(f'Invalid system mode `{mode}`') from exc

        key = f'Switch{mode.title()}Allowed'
        if not self._data['uiData'][key]:
            raise SomeComfortError(f'Device does not support {mode}')
        await self.set_status({'SystemSwitch': mode_index})

    @property
    async def setpoint_cool(self):
        """
        Returns the target temperature when in cooling mode.

        Returns:
            float: The cool setpoint temperature.
        """
        await self.refresh()
        return self._data['uiData']['CoolSetpoint']

    async def set_setpoint_cool(self, temp):
        """
        Sets the cool setpoint temperature.

        Args:
            temp (float): The temperature to set as the cool setpoint.
        """
        await self.refresh()
        lower = self._data['uiData']['CoolLowerSetptLimit']
        upper = self._data['uiData']['CoolUpperSetptLimit']
        if temp > upper or temp < lower:
            raise SomeComfortError(f'Setpoint outside range {lower:.1f}-{upper:.1f}')
        await self.set_status({'CoolSetpoint': temp})

    @property
    async def setpoint_heat(self):
        """
        Returns the target temperature when in heating mode.

        Returns:
            float: The heat setpoint temperature.
        """
        await self.refresh()
        return self._data['uiData']['HeatSetpoint']

    async def set_setpoint_heat(self, temp):
        """
        Sets the heat setpoint temperature.

        Args:
            temp (float): The temperature to set as the heat setpoint.
        """
        await self.refresh()
        lower = self._data['uiData']['HeatLowerSetptLimit']
        upper = self._data['uiData']['HeatUpperSetptLimit']
        if temp > upper or temp < lower:
            raise SomeComfortError(f'Setpoint outside range {lower:.1f}-{upper:.1f}')
        await self.set_status({'HeatSetpoint': temp})

    @property
    async def hold_heat(self):
        """
        Returns the current heat hold mode.

        Returns:
            str: The current hold status for heat.
        """
        return await self._get_hold('Heat')

    async def set_hold_heat(self, value):
        """
        Sets the hold mode for heating.

        Args:
            value (bool or datetime.time): True for permanent hold, False for schedule, or time for temporary hold.
        """
        await self._set_hold('Heat', value)

    @property
    async def hold_cool(self):
        """
        Returns the current cool hold mode.

        Returns:
            str: The current hold status for cooling.
        """
        return await self._get_hold('Cool')

    async def set_hold_cool(self, value):
        """
        Sets the hold mode for cooling.

        Args:
            value (bool or datetime.time): True for permanent hold, False for schedule, or time for temporary hold.
        """
        await self._set_hold('Cool', value)

    async def _set_hold(self, which, hold):
        """
        Sets the hold mode for heating or cooling.

        Args:
            which (str): Either 'Heat' or 'Cool', indicating the system for which to set the hold.
            hold (bool or datetime.time): True for permanent hold, False for schedule, or a time object for temporary hold.

        Raises:
            SomeComfortError: If an invalid hold type or time is provided.
        """
        if hold is True:
            settings = {
                f'Status{which}': HOLD_TYPES.index('permanent'),
                f'{which}NextPeriod': 0,
            }
        elif hold is False:
            settings = {
                f'Status{which}': HOLD_TYPES.index('schedule'),
                f'{which}NextPeriod': 0,
            }
        elif isinstance(hold, datetime.time):
            qh = _hold_quarter_hours(hold)
            settings = {
                f'Status{which}': HOLD_TYPES.index('temporary'),
                f'{which}NextPeriod': qh,
            }
        else:
            raise SomeComfortError('Hold should be True, False, or a datetime.time')

        await self.set_status(settings)

    async def _get_hold(self, which):
        """
        Retrieves the current hold mode for heating or cooling.

        Args:
            which (str): Either 'Heat' or 'Cool', indicating the system for which to get the hold status.

        Returns:
            bool, datetime.time, or None: Returns False if there is no hold, True if there is a permanent hold,
                                        or a time object for a temporary hold.

        Raises:
            APIError: If an unknown hold status is encountered.
        """
        await self.refresh()
        try:
            hold = HOLD_TYPES[self._data['uiData'][f'Status{which}']]
        except KeyError as exc:
            raise APIError(f'Unknown hold mode {self._data["uiData"][f"Status{which}"]}') from exc
        period = self._data['uiData'][f'{which}NextPeriod']
        if hold == 'schedule':
            return False
        elif hold == 'permanent':
            return True
        else:
            return _hold_deadline(period)

    @property
    async def current_temperature(self):
        """
        Returns the current measured ambient temperature.

        Returns:
            float: The current ambient temperature.
        """
        await self.refresh()
        return self._data['uiData']['DispTemperature']

    @property
    async def current_humidity(self):
        """
        Returns the current measured ambient humidity.

        Returns:
            float: The current ambient humidity.
        """
        await self.refresh()
        return self._data['uiData']['IndoorHumidity']

    @property
    async def equipment_output_status(self):
        """
        Returns the current equipment output status.

        Returns:
            str: One of EQUIPMENT_OUTPUT_STATUS, indicating the current output status.
        """
        await self.refresh()
        if self._data['uiData']['EquipmentOutputStatus'] in (0, None):
            if await self.fan_running:
                return "fan"
            else:
                return "off"
        return EQUIPMENT_OUTPUT_STATUS[self._data['uiData']['EquipmentOutputStatus']]

    @property
    async def outdoor_temperature(self):
        """
        Returns the current measured outdoor temperature, if available.

        Returns:
            float or None: The current outdoor temperature or None if not available.
        """
        await self.refresh()
        if self._data['uiData']['OutdoorTemperatureAvailable'] == True:
            return self._data['uiData']['OutdoorTemperature']
        return None

    @property
    async def outdoor_humidity(self):
        """
        Returns the current measured outdoor humidity, if available.

        Returns:
            float or None: The current outdoor humidity or None if not available.
        """
        await self.refresh()
        if self._data['uiData']['OutdoorHumidityAvailable'] == True:
            return self._data['uiData']['OutdoorHumidity']
        return None

    @property
    async def temperature_unit(self):
        """
        Returns the current temperature unit (Fahrenheit or Celsius).

        Returns:
            str: 'F' for Fahrenheit or 'C' for Celsius.
        """
        await self.refresh()
        return self._data['uiData']['DisplayUnits']

    @property
    async def raw_ui_data(self):
        """
        Returns a deep copy of the raw uiData structure from the API.

        Returns:
            dict: A copy of the raw uiData structure.
        """
        await self.refresh()
        return copy.deepcopy(self._data['uiData'])

    @property
    async def raw_fan_data(self):
        """
        Returns a deep copy of the raw fanData structure from the API.

        Returns:
            dict: A copy of the raw fanData structure.
        """
        await self.refresh()
        return copy.deepcopy(self._data['fanData'])

    @property
    async def raw_dr_data(self):
        """
        Returns a deep copy of the raw drData structure from the API.

        Returns:
            dict: A copy of the raw drData structure.
        """
        await self.refresh()
        return copy.deepcopy(self._data['drData'])

    def __repr__(self):
        """
        Returns a string representation of the device.

        Returns:
            str: A string representation showing the device ID and name.
        """
        return f'Device<{self.device_id}:{self.name}>'



# pylint: disable=pointless-string-statement

"""Device Data: {
  "uiData": {
    "DispTemperature": 76.0,
    "HeatSetpoint": 68.0,
    "CoolSetpoint": 76.0,
    "DisplayUnits": "F",
    "StatusHeat": 0,
    "StatusCool": 0,
    "HoldUntilCapable": true,
    "ScheduleCapable": true,
    "VacationHold": 0,
    "DualSetpointStatus": false,
    "HeatNextPeriod": 72,
    "CoolNextPeriod": 72,
    "HeatLowerSetptLimit": 40.0,
    "HeatUpperSetptLimit": 90.0,
    "CoolLowerSetptLimit": 50.0,
    "CoolUpperSetptLimit": 99.0,
    "ScheduleHeatSp": 68.0,
    "ScheduleCoolSp": 76.0,
    "SwitchAutoAllowed": true,
    "SwitchCoolAllowed": true,
    "SwitchOffAllowed": true,
    "SwitchHeatAllowed": true,
    "SwitchEmergencyHeatAllowed": false,
    "SystemSwitchPosition": 3,
    "Deadband": 5.0,
    "IndoorHumidity": 59.0,
    "DeviceID": 3368967,
    "Commercial": false,
    "DispTemperatureAvailable": true,
    "IndoorHumiditySensorAvailable": true,
    "IndoorHumiditySensorNotFault": true,
    "VacationHoldUntilTime": 0,
    "TemporaryHoldUntilTime": 0,
    "IsInVacationHoldMode": false,
    "VacationHoldCancelable": true,
    "SetpointChangeAllowed": true,
    "OutdoorTemperature": 83.0,
    "OutdoorHumidity": 51.0,
    "OutdoorHumidityAvailable": true,
    "OutdoorTemperatureAvailable": true,
    "DispTemperatureStatus": 0,
    "IndoorHumidStatus": 0,
    "OutdoorTempStatus": 0,
    "OutdoorHumidStatus": 0,
    "OutdoorTemperatureSensorNotFault": true,
    "OutdoorHumiditySensorNotFault": true,
    "CurrentSetpointStatus": 0,
    "EquipmentOutputStatus": 0
  },
  "fanData": {
    "fanMode": 1,
    "fanModeAutoAllowed": true,
    "fanModeOnAllowed": true,
    "fanModeCirculateAllowed": true,
    "fanModeFollowScheduleAllowed": false,
    "fanIsRunning": true
  },
  "hasFan": true,
  "canControlHumidification": false,
  "drData": {
    "CoolSetpLimit": null,
    "HeatSetpLimit": null,
    "Phase": -1,
    "OptOutable": false,
    "DeltaCoolSP": null,
    "DeltaHeatSP": null,
    "Load": null
  }
}"""