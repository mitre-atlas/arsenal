from app.objects.c_obfuscator import Obfuscator
from app.utility.base_world import BaseWorld
from plugins.arsenal.app.arsenal_svc import ArsenalService

name = 'Arsenal'
description = 'A plugin of abilities, adversaries, payloads and planners for the ATLAS framework'
address = '/plugin/arsenal/gui'
access = BaseWorld.Access.APP

async def enable(services):
    arsenal_svc = ArsenalService(services)
    services.get('app_svc').application.router.add_route('GET', '/plugin/arsenal/gui', arsenal_svc.splash)
    await services.get('file_svc').add_special_payload('.donut', 'plugins.arsenal.app.donut.donut_handler')
    await arsenal_svc.data_svc.store(
        Obfuscator(name='plain-text',
                   description='Does no obfuscation to any command, instead running it in plain text',
                   module='plugins.arsenal.app.obfuscators.plain_text')
    )
    await arsenal_svc.data_svc.store(
        Obfuscator(name='base64',
                   description='Obfuscates commands in base64',
                   module='plugins.arsenal.app.obfuscators.base64_basic')
    )
    await arsenal_svc.data_svc.store(
        Obfuscator(name='base64jumble',
                   description='Obfuscates commands in base64, then adds characters to evade base64 detection. '
                               'Disclaimer: this may cause duplicate links to run.',
                   module='plugins.arsenal.app.obfuscators.base64_jumble')
    )
    await arsenal_svc.data_svc.store(
        Obfuscator(name='caesar cipher',
                   description='Obfuscates commands through a caesar cipher algorithm, which uses a randomly selected '
                               'shift value.',
                   module='plugins.arsenal.app.obfuscators.caesar_cipher')
    )
    await arsenal_svc.data_svc.store(
        Obfuscator(name='base64noPadding',
                   description='Obfuscates commands in base64, then removes padding',
                   module='plugins.arsenal.app.obfuscators.base64_no_padding')
    )
    await arsenal_svc.data_svc.store(
        Obfuscator(name='steganography',
                   description='Obfuscates commands through image-based steganography',
                   module='plugins.arsenal.app.obfuscators.steganography')
    )
