from app.objects.c_obfuscator import Obfuscator
from app.utility.base_world import BaseWorld
from plugins.stockpile.app.stockpile_svc import StockpileService

name = 'Stockpile'
description = 'A stockpile of abilities, adversaries, payloads and planners'
address = '/plugin/stockpile/gui'
access = BaseWorld.Access.RED


async def enable(services):
    stockpile_svc = StockpileService(services)
    services.get('app_svc').application.router.add_route('GET', '/plugin/stockpile/gui', stockpile_svc.splash)
    await stockpile_svc.data_svc.store(
        Obfuscator(name='plain-text',
                   description='Does no obfuscation to any command, instead running it in plain text',
                   module='plugins.stockpile.app.obfuscators.plain_text')
    )
    await stockpile_svc.data_svc.store(
        Obfuscator(name='base64',
                   description='Obfuscates commands in base64',
                   module='plugins.stockpile.app.obfuscators.base64_basic')
    )
    await stockpile_svc.data_svc.store(
        Obfuscator(name='base64jumble',
                   description='Obfuscates commands in base64, then adds characters to evade base64 detection. '
                               'Disclaimer: this may cause duplicate links to run.',
                   module='plugins.stockpile.app.obfuscators.base64_jumble')
    )
    await stockpile_svc.data_svc.store(
        Obfuscator(name='base64noPadding',
                   description='Obfuscates commands in base64, then removes padding',
                   module='plugins.stockpile.app.obfuscators.base64_no_padding')
    )
