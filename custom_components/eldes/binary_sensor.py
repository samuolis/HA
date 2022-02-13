from homeassistant.config_entries import ConfigEntry
from homeassistant.const import STATE_ON, STATE_OFF, DEVICE_CLASS_BATTERY
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import CoordinatorEntity, DataUpdateCoordinator

import logging
from datetime import timedelta

from .const import DOMAIN, COORDINATOR

from eldes import EldesClient

_LOGGER = logging.getLogger(__name__)

POLLING_TIMEOUT_SEC = 10
UPDATE_INTERVAL = timedelta(seconds=30)


async def async_setup_entry(
        hass: HomeAssistant, config_entry: ConfigEntry, async_add_devices
):
    api: EldesClient = hass.data[DOMAIN][COORDINATOR]

    name="Eldes-arm-coordinator"

    async def async_update_data():
        """Fetch data from the subdevice using async_add_executor_job."""
        return await hass.async_add_executor_job(update_data)

    def update_data():
        """Fetch data for alarm"""
        return api.is_partition_armed(location="Home", partition="Namai")

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=name,
        update_method=async_update_data,
        # Polling interval. Will only be polled if there are subscribers.
        update_interval=UPDATE_INTERVAL,
    )
    async_add_devices(EldesSecurityBinarySensor(
        coordinator=coordinator,
        id="eldes-security",
        device_class=None
    ), True)


class EldesSecurityBinarySensor(CoordinatorEntity):
    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        id: str,
        device_class,
    ):
        super().__init__(coordinator)
        self._id = id
        self._device_class = device_class

        _LOGGER.debug(
            f"{DOMAIN} - binary init -"
        )

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.device.serial_number)},
            "name": "Eldes alarm",
            "model": "-",
            "hardware": "-",
            "software": "-",
            "manufacturer": "ELDES",
        }

    @property
    def available(self) -> bool:
        return self.coordinator.data

    @property
    def should_poll(self) -> bool:
        return False

    @property
    def is_on(self):
        value = self.available
        return bool(value)

    @property
    def state(self):
        return STATE_ON if self.is_on else STATE_OFF

    @property
    def device_class(self):
        return self._device_class

    @property
    def name(self):
        return "Eldes security"

    @property
    def id(self):
        return f"{DOMAIN}_{self._id}_binary_sensor"

    @property
    def unique_id(self):
        return self.id
