"""The Shelly 3m API-Emulator."""

import json

from aiohttp import web


async def handle_rpc(request):
    hass = request.app["hass"]
    data = hass.data["shelly_3em_emulator_4mqtt"]["energy_data"]

    response = {
        "id": 0,
        "src": "shellypro3em-emu",
        "result": {
            "a_voltage": data["a_voltage"],
            "a_power": data["a_power"],
            "b_power": data["b_power"],
            "c_power": data["c_power"],
            "total_power": data["total"],
        },
    }

    return web.Response(text=json.dumps(response), content_type="application/json")


async def start_api_server(hass):
    app = web.Application()
    app["hass"] = hass
    app.router.add_get("/rpc/Switch.GetStatus", handle_rpc)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 80)  # Port 80 für Shelly-Kompatibilität
    await site.start()
