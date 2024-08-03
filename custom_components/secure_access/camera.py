from __future__ import annotations

from typing import Any

from homeassistant.components.camera import Camera, CameraEntityFeature
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

class ASCamera(Camera):

    _attr_supported_features = CameraEntityFeature.STREAM

    def __init__(self, panel: AccessPanel):
        self._panel = panel
        self._attr_unique_id = f"{self._panel.panel_id}_camera"
        self._attr_name = self._panel.name
    
    async def stream_source(self) -> str | None:
        return "rtsp://demo:demo@ipvmdemo.dyndns.org:5541/onvif-media/media.amp?profile=profile_1_h264&sessiontimeout=60&streamtype=unicast"