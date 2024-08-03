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
        pass

    async def stream_source(self) -> str | None:
        return "https://nasa-i.akamaihd.net/hls/live/253565/NTV-Public1/master.m3u8"