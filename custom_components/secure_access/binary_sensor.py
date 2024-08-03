from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import DiscoveryInfoType

from .const import DOMAIN
from .access_server import AccessServer, AccessPanel

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    access_server: AccessServer = hass.data[DOMAIN][config_entry.entry_id]

    new_devices = []
    for panel in access_server.panels:
        new_devices.append(DoorSensor(panel))
        new_devices.append(BypassSensor(panel))
    if new_devices:
        async_add_entities(new_devices)

class SensorBase(BinarySensorEntity):
    should_poll = False

    def __init__(self, panel):
        self._panel = panel

    @property
    def device_info(self):
        return {"identifers": {(DOMAIN, self._panel.panel_id)}}
    
    @property
    def available(self) -> bool:
        return self._panel.online and self._panel.server.online
    
    async def async_added_to_hass(self):
        self._panel.register_callback(self.async_write_ha_state)

    async def async_will_remove_from_hass(self):
        self._panel.remove_callback(self.async_write_ha_state)

class DoorSensor(SensorBase):
    _attr_device_class = BinarySensorDeviceClass.DOOR
    
    def __init__(self, panel):
        super().__init__(panel)

        self._attr_unique_id = f"{self._panel.panel_id}_lock"
        self._attr_name = f"{self._panel.name} Lock"
        self._attr_state = self._panel.door_state
    
    @property
    def state(self):
        return self._panel.door_state

class BypassSensor(SensorBase):
    _attr_device_class = BinarySensorDeviceClass.SAFETY
    _attr_name = "Bypass Sensor"
    
    def __init__(self, panel):
        super().__init__(panel)

        self._attr_unique_id = f"{self._panel.panel_id}_bypass"
        self._attr_state = self._panel.is_bypassed
    
    @property
    def state(self):
        return self._panel.is_bypassed