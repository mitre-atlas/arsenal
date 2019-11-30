from plugins.stockpile.app.http import HTTP
from plugins.stockpile.app.stockpile_svc import StockpileService

name = 'Stockpile'
description = 'A stockpile of abilities, adversaries, payloads and planners'
address = None


async def enable(services):
    file_svc = services.get('file_svc')
    await file_svc.add_special_payload('mission.go', StockpileService(file_svc).dynamically_compile)

    data_svc = services.get('data_svc')
    await data_svc.load_data(directory='plugins/stockpile/data')
    await services.get('contact_svc').register(HTTP(services))
