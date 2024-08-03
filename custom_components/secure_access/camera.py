from __future__ import annotations

from typing import Any

from homeassistant.components.mjpeg import MjpegCamera
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN

from .access_server import AccessServer, AccessPanel


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    acs: AccessServer = hass.data[DOMAIN][config_entry.entry_id]

    async_add_entities([ASCamera(panel) for panel in acs.panels])

class ASCamera(MjpegCamera):

    _attr_has_entity_name = True

    def __init__(self, panel: AccessPanel):
        super().__init__(
            mjpeg_url="http://80.56.142.202:83/mjpg/video.mjpg?camera=1",
            still_image_url="http://80.56.142.202:83/mjpg/video.mjpg?camera=1&timestamp=1722723200017"
        )
        self._attr_unique_id = f"{panel.panel_id}_camera"
        self._attr_name = panel.name