import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import asyncio
import logging
from asyncsomecomfort.client import Client

# Configure logging
logging.basicConfig(level=logging.DEBUG)
_LOGGER = logging.getLogger(__name__)

# User credentials (replace with actual test credentials)
username = "mike@4831.com"
password = "Cdiv2012"

async def handle_device_change(device, data):
    _LOGGER.info(f"Device {device.name} changed: {data}")

async def main():
    async with Client(username, password) as client:
        devices_of_interest = []

        # Access devices from all locations
        for location in client._locations.values():
            async with location:
                devices = location.devices
                devices_of_interest.extend(devices.values())

        # Register listeners and start polling
        for device in devices_of_interest:
            device.on_change(lambda data, dev=device: asyncio.create_task(handle_device_change(dev, data)))
            await device.start_polling(interval=120)

        try:
            # Keep the program running
            while True:
                await asyncio.sleep(3600)
        except KeyboardInterrupt:
            _LOGGER.info("Stopping monitoring...")
        finally:
            # Stop polling on all devices
            for device in devices_of_interest:
                await device.stop_polling()

if __name__ == "__main__":
    asyncio.run(main())