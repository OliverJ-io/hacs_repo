from __future__ import annotations

import asyncio
import random
from typing import Callable

from homeassistant.core import HomeAssistant

class AccessServer:
    def __init__(self, hass: HomeAssistant, ip: str) -> None:
        self._ip = ip
        self._hass = hass
        self._name = "Access Server"
        self._id = self._name.replace(" ", "_").lower() + "_" + random.randbytes(4).hex()
        self.panels = [
            AccessPanel(f"{self._id}_1", f"Panel 1", self),
            AccessPanel(f"{self._id}_2", f"Panel 2", self),
            AccessPanel(f"{self._id}_3", f"Panel 3", self)
        ]
        self.online = True

    @property
    def hub_id(self) -> str:
        return self._id
    
    async def test_connection(self) -> bool:
        await asyncio.sleep(1)
        return self.online
    
class AccessPanel:
    def __init__(self, panel_id: str, name: str, server: AccessServer) -> None:
        self._id = panel_id
        self.server = server
        self.name = name
        self._callbacks = set()
        self._loop = asyncio.get_event_loop()
        self._door_state = False
        self._is_bypassed = False

        self.firmware_version = f"0.0.1"
        self.model = "OliverJ Access Panel"
    
    @property
    def panel_id(self) -> str:
        return self._id
    
    @property
    def door_state(self) -> bool:
        return self._door_state
    
    @property
    def is_bypassed(self) -> bool:
        return self._is_bypassed
    
    def register_callback(self, callback: Callable[[], None]) -> None:
        self._callbacks.add(callback)

    def remove_callback(self, callback: Callable[[], None]) -> None:
        self._callbacks.discard(callback)

    async def publish_updates(self) -> None:
        for callback in self._callbacks:
            callback()

    @property
    def online(self) -> float:
        return False