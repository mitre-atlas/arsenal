from app.objects.c_obfuscator import Obfuscator
from plugins.stockpile.app.contact.gist import Gist
from plugins.stockpile.app.stockpile_svc import StockpileService

name = 'Stockpile'
description = 'A stockpile of abilities, adversaries, payloads and planners'
address = None


async def enable(services):
    stockpile_svc = StockpileService(services)
    stockpile_svc.data_svc.data_dirs.add('plugins/stockpile/data')
    await services.get('contact_svc').register(Gist(services=services))

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
