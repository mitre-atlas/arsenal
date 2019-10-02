from plugins.stockpile.app.stockpile_api import StockpileApi

name = 'Stockpile'
description = 'A stockpile of abilities, adversaries, payloads and planners'
address = None


async def initialize(app, services):
    stockpile_api = StockpileApi(services)
    data_svc = services.get('data_svc')
    parsing_svc = services.get('parsing_svc')
    app.router.add_route('POST', '/stockpile/ability', stockpile_api.load_ability)
    await data_svc.load_data(directory='plugins/stockpile/data')
    await parsing_svc.load_parsers(directory='plugins/stockpile/parsers')
