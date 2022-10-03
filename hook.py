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
