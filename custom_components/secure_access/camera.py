from __future__ import annotations

from typing import Any

from homeassistant.components.camera import (
    Camera,
    CameraEntityFeature,
    StreamType
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add cover for passed config_entry in HA."""
    # The hub is loaded from the associated hass.data entry that was created in the
    # __init__.async_setup_entry function
    hub = hass.data[DOMAIN][config_entry.entry_id]

    # Add all entities to HA
    async_add_entities(ASCamera(panel) for panel in hub.panel)

class ASCamera(Camera):

    _attr_supported_features = CameraEntityFeature.STREAM

    def __init__(self, panel):
        self._panel = panel
        self._attr_unique_id = f"{self._panel.panel_id}_camera"
        self._attr_name = self._panel.name

    async def async_added_to_hass(self) -> None:
        self._panel.register_callback(self.async_write_ha_state)

    async def async_will_remove_from_hass(self) -> None:
        self._roller.remove_callback(self.async_write_ha_state)

    @property
    def device_info(self) -> dict:
        return {
            "identifiers": {(DOMAIN, self._panel.panel_id)},
            "name": self.name,
            "sw_version": self._panel.firmware_version,
            "model": self._panel.model,
            "manufacturer": self._panel.server.manufacturer
        }
    
    @property
    def available(self) -> bool:
        return self._panel.online and self._panel.server.online

    async def stream_source(self) -> str | None:
        return "https://demo.unified-streaming.com/k8s/features/stable/video/tears-of-steel/tears-of-steel.ism/.m3u8"