#main.py
"""Fluss+ API Client."""

from __future__ import annotations

import asyncio
import datetime
import logging
import socket
import typing
import aiohttp

from aiohttp import ClientSession
from homeassistant.helpers import aiohttp_client # type: ignore

LOGGER = logging.getLogger(__package__)



class FlussApiClientError(Exception):
    """Exception to indicate a general API error."""


class FlussDeviceError(Exception):
    """Exception to indicate that an error occurred when retrieving devices."""


class FlussApiClientCommunicationError(FlussApiClientError):
    """Exception to indicate a communication error."""


class FlussApiClientAuthenticationError(FlussApiClientError):
    """Exception to indicate an authentication error."""


class FlussApiClient:
    """Fluss+ API Client."""

    def __init__(self, api_key: str, hass: HomeAssistant = None) -> None:
        """Initialize the Fluss+ API Client."""
        self._api_key = api_key
        self._session: ClientSession = aiohttp_client.async_get_clientsession(hass) if hass else ClientSession()

    async def async_get_devices(self) -> typing.Any:
        """Get data from the API."""
        try:
            return await self._api_wrapper(
                method="GET",
                url="https://zgekzokxrl.execute-api.eu-west-1.amazonaws.com/v1/api/device/list",
                headers={"Authorization": self._api_key},
            )
        except FlussApiClientError as error:
            LOGGER.error("Failed to get devices: %s", error)
            raise FlussDeviceError("Failed to retrieve devices") from error

    async def async_trigger_device(self, deviceId: str) -> typing.Any:
        """Trigger the device."""
        timestamp = int(datetime.datetime.now().timestamp() * 1000)
        return await self._api_wrapper(
            method="POST",
            url=f"https://zgekzokxrl.execute-api.eu-west-1.amazonaws.com/v1/api/device/{deviceId}/trigger",
            headers={"Authorization": self._api_key},
            data={"timeStamp": timestamp, "metaData": {}},
        )


    async def _api_wrapper(
        self,
        method: str,
        url: str,
        data: dict | None = None,
        headers: dict | None = None,
    ) -> typing.Any:
        """Get information from the API."""
        try:
            async with asyncio.timeout(10):
                response = await self._session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=data,
                )
                if response.status in (401, 403):
                    raise FlussApiClientAuthenticationError("Invalid credentials")
                response.raise_for_status()
                return await response.json()

        except asyncio.TimeoutError as e:
            LOGGER.error("Timeout error fetching information from %s", url)
            raise FlussApiClientCommunicationError("Timeout error fetching information") from e
        except (aiohttp.ClientError, socket.gaierror) as ex:
            LOGGER.error("Error fetching information from %s: %s", url, ex)
            raise FlussApiClientCommunicationError("Error fetching information") from ex
        except FlussApiClientAuthenticationError as auth_ex:
            LOGGER.error("Authentication error: %s", auth_ex)
            raise
        except Exception as exception:  # pylint: disable=broad-except
            LOGGER.error("Unexpected error occurred: %s", exception)
            raise FlussApiClientError("Something really wrong happened!") from exception

    async def close(self):
        """Close the aiohttp session."""
        if self._session:
            await self._session.close()