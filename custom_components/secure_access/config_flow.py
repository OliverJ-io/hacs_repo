from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant import exceptions
from .const import DOMAIN
from .access_server import AccessServer

from typing import Any
import logging

import voluptuous as vol
import ipaddress

_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA = vol.Schema({vol.Required("ip"): str, vol.Optional("checkbox"): bool})

async def validate_input(hass: HomeAssistant, data: dict) -> dict[str, Any]:
    try:
        ip = ipaddress.ip_address(data["ip"])
    except ValueError:
        raise InvalidIp
    
    if data["checkbox"] == False:
        raise NoTOS
    
    access_server = AccessServer(hass, data["ip"])

    result = await access_server.test_connection()
    if not result:
        raise ASConnectFailed
    
    return {"title": data["ip"]}

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):

    VERSION = 1
    MINOR_VERSION = 0

    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_PUSH

    async def async_step_user(self, user_input=None):

        errors = {}

        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)

                return self.async_create_entry(title=info["title"], data=user_input)
            except ASConnectFailed:
                errors["base"] = "connection_failed"
            except InvalidIP:
                errors["ip"] = "invalid_ip"
            except NoTOS:
                errors["checkbox"] = "no_agreement"
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )

class ASConnectFailed(exceptions.HomeAssistantError):
    """"""

class InvalidIp(exceptions.HomeAssistantError):
    """"""

class NoTOS(exceptions.HomeAssistantError):
    """"""