"""Config flow for the Shelly 3m Emulator for MQTT integration."""

# import my_pypi_dependency
import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_PASSWORD, CONF_PORT, CONF_USERNAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_entry_flow, config_validation as cv

from .const import (
    CONF_MQTT_BROKER,
    CONF_MQTT_POWER_PHASE1_TOPIC,
    CONF_MQTT_POWER_PHASE2_TOPIC,
    CONF_MQTT_POWER_PHASE3_TOPIC,
    CONF_MQTT_POWER_PHASEALL_TOPIC,
    CONF_MQTT_POWER_TOPIC,
    DEFAULT_MQTT_PORT,
    DOMAIN,
)

SCHEMA_DEVICE = vol.Schema(
    {
        vol.Required(CONF_MQTT_BROKER): cv.string,
        vol.Required(CONF_MQTT_POWER_TOPIC): cv.string,
        vol.Required(CONF_PORT, default=DEFAULT_MQTT_PORT): cv.port,
        vol.Optional(CONF_USERNAME, default=""): cv.string,
        vol.Optional(CONF_PASSWORD, default=""): cv.string,
        vol.Required(CONF_MQTT_POWER_PHASE1_TOPIC): cv.string,
        vol.Required(CONF_MQTT_POWER_PHASE2_TOPIC): cv.string,
        vol.Required(CONF_MQTT_POWER_PHASE3_TOPIC): cv.string,
        vol.Optional(CONF_MQTT_POWER_PHASEALL_TOPIC): cv.string,
    }
)


class Shelly3memulator4mqttFlowHandler(ConfigFlow, domain=DOMAIN):
    """Config flow for Shelly 3m Emulator for MQTT integration."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, vol.Any] | None = None
    ) -> ConfigFlowResult:
        """Handle a flow initialized by the user."""
        errors = {}

        if user_input is not None:
            broker = user_input[CONF_MQTT_BROKER]
            topic = user_input[CONF_MQTT_POWER_TOPIC]

            await self.async_set_unique_id(str(broker) + str(topic))
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=f"Shelly 3m Emulator - MQTT-Broker: {broker}, Topic: {topic}",
                data=user_input,
            )

        return self.async_show_form(
            step_id="user",
            data_schema=SCHEMA_DEVICE,
            errors=errors,
        )

