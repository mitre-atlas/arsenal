from plugins.stockpile.app.stockpile_api import StockpileApi
from plugins.stockpile.app.stockpile_svc import StockpileService

name = 'Stockpile'
description = 'A stockpile of abilities, adversaries, payloads and planners'
address = None


async def initialize(app, services):
    file_svc = services.get('file_svc')
    await file_svc.add_special_payload('mission.go', StockpileService(file_svc).dynamically_compile)

    stockpile_api = StockpileApi(services)
    data_svc = services.get('data_svc')
    app.router.add_route('POST', '/stockpile/ability', stockpile_api.load_ability)
    await data_svc.load_data(directory='plugins/stockpile/data')
