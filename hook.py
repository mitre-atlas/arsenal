name = 'Stockpile'
description = 'A stockpile of abilities, adversaries, payloads and planners'
address = None


async def initialize(app, services):
    data_svc = services.get('data_svc')
    await data_svc.reload_database(adversaries='plugins/stockpile/adversaries.yml',
                                   abilities='plugins/stockpile/abilities',
                                   facts='plugins/stockpile/facts.yml',
                                   planner=dict(name='sequential', module='plugins.stockpile.app.sequential'))
