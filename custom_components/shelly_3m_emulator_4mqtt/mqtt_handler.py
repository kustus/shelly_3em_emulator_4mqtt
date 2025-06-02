"""The MQTT handler for data input."""

import logging

_LOGGER = logging.getLogger(__name__)

TOPIC = "dein/mqtt/topic"  # z. B. von einem echten Energiezähler


async def setup_mqtt(hass):
    async def message_received(msg):
        try:
            payload = msg.payload
            data = hass.data["shelly_3em_emulator_mqtt"]["energy_data"]

            # Beispiel: MQTT-Daten verarbeiten
            # Erwarte JSON wie: {"voltage":230,"power_a":1000,"power_b":500,"power_c":200}
            import json

            incoming = json.loads(payload)

            data["a_voltage"] = incoming.get("voltage", 230.0)
            data["a_power"] = incoming.get("power_a", 0.0)
            data["b_power"] = incoming.get("power_b", 0.0)
            data["c_power"] = incoming.get("power_c", 0.0)
            data["total"] = data["a_power"] + data["b_power"] + data["c_power"]

        except Exception as e:
            _LOGGER.error(f"Fehler beim Verarbeiten der MQTT-Nachricht: {e}")

    await hass.components.mqtt.async_subscribe(TOPIC, message_received)
