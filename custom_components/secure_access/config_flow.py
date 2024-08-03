from homeassistant import config_entries
from .const import DOMAIN

import voluptuous as vol

DATA_SCHEMA = vol.Schema({vol.Required("ip"): str, vol.Optional("checkbox"): bool})

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, info):
        if info is not None:
            pass

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA
        )
    
    async def async_set_unignore(self, user_input):
        unique_id = user_input["unique_id"]
        await self.async_set_unique_id(unique_id)

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA
        )