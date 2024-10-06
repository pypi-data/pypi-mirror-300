import logging
from typing import Any, Dict, Optional

import aiohttp

from .const import DEFAULT_API_URL
from .exceptions import (
    DeviceOfflineError,
    ApiError,
)

_LOGGER = logging.getLogger(__name__)


class AppartmePaasClient:
    """Client for Appartme PaaS API."""

    def __init__(
            self,
            access_token: str,
            session: Optional[aiohttp.ClientSession] = None,
            api_url: Optional[str] = DEFAULT_API_URL
            ):
        """Initialize the AppartmePaasClient.

        Args:
            access_token (str): OAuth2 access token.
            session (aiohttp.ClientSession, optional): aiohttp session.
            api_url (str): URL address for Appartme PaaS API
        """
        self.base_url = api_url
        self.access_token = access_token
        self.session = session or aiohttp.ClientSession()

    async def close(self):
        """Close the aiohttp session if it was created by the client."""
        if self.session and not self.session.closed:
            await self.session.close()

    async def fetch_devices(self) -> Dict[str, Any]:
        """Fetch the list of devices."""
        url = f"{self.base_url}/devices"
        headers = {"Authorization": f"Bearer {self.access_token}"}

        async with self.session.get(url, headers=headers) as response:
            if response.status != 200:
                error_message = await response.text()
                _LOGGER.error(
                    "Error fetching devices: %s, %s", response.status, error_message
                )
                raise ApiError(f"Error fetching devices: {response.status}, {error_message}")
            return await response.json()

    async def fetch_device_details(self, device_id: str) -> Dict[str, Any]:
        """Fetch details of a specific device."""
        url = f"{self.base_url}/devices/{device_id}"
        headers = {"Authorization": f"Bearer {self.access_token}"}

        async with self.session.get(url, headers=headers) as response:
            if response.status != 200:
                error_message = await response.text()
                _LOGGER.error(
                    "Error fetching device %s details: %s", device_id, error_message
                )
                raise ApiError(
                    f"Error fetching device {device_id} details: {response.status}, {error_message}"
                )
            return await response.json()

    async def set_device_property_value(
        self, device_id: str, property: str, value: Any
    ) -> Dict[str, Any]:
        """Set a device property value."""
        url = f"{self.base_url}/devices/{device_id}/property/{property}/value"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        payload = {"value": value}

        async with self.session.patch(url, headers=headers, json=payload) as response:
            if response.status == 504:
                _LOGGER.error("Device %s is offline when setting property %s", device_id, property)
                raise DeviceOfflineError(
                    f"Device {device_id} is offline when setting property {property}"
                )
            if response.status != 200:
                error_message = await response.text()
                _LOGGER.error("Error setting property %s: %s", property, error_message)
                raise ApiError(
                    f"Error setting property {property} for device {device_id}: {response.status}, {error_message}"
                )
            return await response.json()

    async def get_device_property_value(
        self, device_id: str, property: str
    ) -> Dict[str, Any]:
        """Get a device property value."""
        url = f"{self.base_url}/devices/{device_id}/property/{property}/value"
        headers = {"Authorization": f"Bearer {self.access_token}"}

        async with self.session.get(url, headers=headers) as response:
            if response.status == 504:
                _LOGGER.error("Device %s is offline when fetching property %s", device_id, property)
                raise DeviceOfflineError(
                    f"Device {device_id} is offline when fetching property {property}"
                )
            if response.status != 200:
                error_message = await response.text()
                _LOGGER.error("Error fetching property %s: %s", property, error_message)
                raise ApiError(
                    f"Error fetching property {property} for device {device_id}: {response.status}, {error_message}"
                )
            return await response.json()

    async def get_device_properties(self, device_id: str) -> Dict[str, Any]:
        """Fetch all properties of a device."""
        url = f"{self.base_url}/devices/{device_id}/property"
        headers = {"Authorization": f"Bearer {self.access_token}"}

        async with self.session.get(url, headers=headers) as response:
            if response.status == 504:
                _LOGGER.error("Device %s is offline when fetching properties", device_id)
                raise DeviceOfflineError(
                    f"Device {device_id} is offline when fetching properties"
                )
            if response.status != 200:
                error_message = await response.text()
                _LOGGER.error("Error fetching properties: %s", error_message)
                raise ApiError(
                    f"Error fetching properties for device {device_id}: {response.status}, {error_message}"
                )
            return await response.json()
