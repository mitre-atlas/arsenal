from app.objects.c_obfuscator import Obfuscator
from plugins.stockpile.app.contact.gist import GIST
from plugins.stockpile.app.stockpile_svc import StockpileService

name = 'Stockpile'
description = 'A stockpile of abilities, adversaries, payloads and planners'
address = None


async def enable(services):
    stockpile_svc = StockpileService(services)
    await stockpile_svc.file_svc.add_special_payload('mission.go', stockpile_svc.dynamically_compile)
    await stockpile_svc.data_svc.load_data(directory='plugins/stockpile/data')

    c2_configs = await stockpile_svc.load_c2_config(directory='plugins/stockpile/data/contact')
    await stockpile_svc.contact_svc.register(GIST(services, c2_configs['GIST']))
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
