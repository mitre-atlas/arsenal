name = 'Stockpile'
description = 'A stockpile of abilities, adversaries and files'
address = None
store = 'plugins/stockpile/filestore'


async def initialize(app, services):
    data_svc = services.get('data_svc')
    await data_svc.reload_database(adversaries='plugins/stockpile/adversaries.yml',
                                   abilities='plugins/stockpile/abilities')
