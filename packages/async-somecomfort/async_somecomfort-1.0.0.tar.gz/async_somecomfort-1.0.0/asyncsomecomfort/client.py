"""
This module provides the Client class to interact with the session and locations
in the SomeComfort API. The Client class handles authentication, location discovery,
and device management through asynchronous methods.

Classes:
    Client: Manages session, location discovery, and device retrieval.
"""

import logging
from .session import Session
from .location import Location

_LOG = logging.getLogger("somecomfort")


class Client:
    """
    A client class to handle the session and interaction with the API.
    """

    def __init__(self, username, password, timeout=30):
        """
        Initializes the Client with user credentials and session timeout.

        :param username: Username for authentication
        :param password: Password for authentication
        :param timeout: Timeout duration for the session, default is 30
        """
        self._session = Session(username, password, timeout)
        self._locations = {}

    async def __aenter__(self):
        """
        Async context manager entry method.

        :return: Client instance
        """
        await self._session.__aenter__()
        await self._discover_locations()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Async context manager exit method.

        :param exc_type: Exception type
        :param exc_val: Exception value
        :param exc_tb: Exception traceback
        """
        await self._session.__aexit__(exc_type, exc_val, exc_tb)

    async def _discover_locations(self):
        """
        Discovers and processes available locations for the user.
        """
        try:
            await self._session.login()  # Call the appropriate login method after fixing the protected access issue
            _LOG.info("Starting discovery process...")
            raw_locations = await self._session.get_locations()
            _LOG.info("Retrieved %d locations", len(raw_locations))  # Lazy string formatting
            for raw_location in raw_locations:
                try:
                    location = Location(self._session, raw_location)
                    self._locations[location.location_id] = location
                    _LOG.info("Processed location: %s", location.location_id)  # Lazy formatting
                    await location.get_devices()
                except KeyError as ex:
                    _LOG.error(
                        "Failed to process location `%s`: missing %s element",
                        raw_location.get('LocationID', 'unknown'),
                        ex.args[0]
                    )
                except ValueError as ve:  # Example of a more specific error
                    _LOG.error("ValueError processing location: %s", str(ve))
                # You can add more specific exceptions here if needed
        except (ConnectionError, TimeoutError) as e:  # Specific exceptions you expect
            _LOG.error("Network error in _discover: %s", str(e), exc_info=True)
            raise
        except Exception as e:
            _LOG.error("Unexpected error in _discover: %s", str(e), exc_info=True)
            raise

    @property
    def locations_by_id(self):
        """
        Returns the dictionary of locations by their ID.

        :return: Dictionary of locations
        """
        return self._locations

    @property
    async def default_device(self):
        """
        Returns the default device from the first location, if available.

        :return: The default device or None if not found
        """
        for location in self.locations_by_id.values():
            for device in location.devices_by_id.values():
                return device
        return None

    async def get_device(self, device_id):
        """
        Retrieves a device by its ID.

        :param device_id: ID of the device to retrieve
        :return: Device if found, otherwise None
        """
        for location in self.locations_by_id.values():
            for ident, device in location.devices_by_id.items():
                if ident == device_id:
                    return device
        return None

    async def close(self):
        """
        Closes the session.
        """
        await self._session.close()
