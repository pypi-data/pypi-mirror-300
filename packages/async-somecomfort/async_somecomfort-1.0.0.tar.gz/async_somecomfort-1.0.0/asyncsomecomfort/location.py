"""
Module: location.py
This module contains the implementation of the Location class, 
which represents a Honeywell TCC location.

Classes:
    Location: Represents a Honeywell TCC location and its associated devices.

Methods:
    __init__(self, session, data): Initializes a Location object with session and data.
    __aenter__(self): Asynchronous context manager enter method to refresh devices.
    __aexit__(self, exc_type, exc_val, exc_tb): Asynchronous context manager exit method.
    _init_devices(self, devices_data): Initializes devices from the location data.
    refresh_devices(self): Asynchronously refreshes the devices associated with the location.
    get_devices(self): Returns a list of devices associated with this location.
    get_device_by_id(self, device_id): Returns a specific device by its ID.
    __repr__(self): Returns a string representation of the Location object.
"""

import logging
import json
from .exceptions import SomeComfortError
from .device import Device

_LOGGER = logging.getLogger(__name__)

class Location:
    """
    Represents a Honeywell TCC location and manages the devices within that location.

    Attributes:
        _session (Session): The session used to communicate with the API.
        location_id (str): The unique ID of the location.
        devices (dict): A dictionary of devices associated with the location, keyed by device ID.
        _raw_data (dict): The raw location data provided during initialization.
    """

    def __init__(self, session, data):
        """
        Initializes a Location object with session and data.

        Args:
            session (Session): The session used for API communication.
            data (dict): The location data containing details about the location and devices.
        """
        self._session = session
        self.location_id = data["LocationID"]
        self.devices = {}
        self._raw_data = data
        self._init_devices(data.get("Devices", []))

        _LOGGER.debug("Initialized Location ID: %s", self.location_id)
        _LOGGER.debug("Location Settings: %s", json.dumps(data, indent=2))

    async def __aenter__(self):
        """
        Asynchronous context manager entry method.

        Refreshes the devices associated with the location upon entering the context.
        
        Returns:
            Location: The current Location instance.
        """
        await self.refresh_devices()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Asynchronous context manager exit method.

        No specific cleanup actions are needed, so this method passes without action.
        """
        pass

    def _init_devices(self, devices_data):
        """
        Initializes devices from the location data and stores them in the devices dictionary.

        Args:
            devices_data (list): A list of device data to initialize Device objects.
        """
        for device_data in devices_data:
            device = Device(self._session, device_data)
            self.devices[device.device_id] = device
            _LOGGER.info("Initialized device: %s", device.name)

    async def refresh_devices(self):
        """
        Asynchronously refreshes the devices associated with the location by calling
        the `refresh` method on each device.

        Raises:
            SomeComfortError: If there is an issue refreshing the devices.
        """
        try:
            for device in self.devices.values():
                await device.refresh()
            _LOGGER.info("Refreshed devices for location ID %s", self.location_id)
        except SomeComfortError as e:
            _LOGGER.error("Error refreshing devices: %s", e)
            raise

    async def get_devices(self):
        """
        Asynchronously retrieves the list of devices associated with this location.

        Returns:
            list: A list of Device objects associated with this location.
        """
        return list(self.devices.values())

    def get_device_by_id(self, device_id):
        """
        Retrieves a specific device by its device ID.

        Args:
            device_id (str): The unique ID of the device.

        Returns:
            Device: The device associated with the given ID, or None if not found.
        """
        return self.devices.get(device_id)

    def __repr__(self):
        """
        Returns a string representation of the Location object.

        Returns:
            str: A string showing the location ID.
        """
        return f"<Location ID {self.location_id}>"
