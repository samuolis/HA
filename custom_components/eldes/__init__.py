"""The Eldes security integration."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from eldes import EldesClient
from .const import DOMAIN, HOST_DEVICE_ID, USERNAME, PASSWORD, COORDINATOR

PLATFORMS = [Platform.BINARY_SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Eldes security from a config entry."""
    hass.data[DOMAIN][COORDINATOR] = EldesClient(
        hostDeviceId=entry.data.get(HOST_DEVICE_ID),
        username=entry.data.get(USERNAME),
        password=entry.data.get(PASSWORD)
    )

    hass.config_entries.async_setup_platforms(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
