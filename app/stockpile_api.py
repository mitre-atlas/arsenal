import os

from aiohttp import web
from pathlib import Path


class StockpileApi:

    def __init__(self, services):
        self.services = services

    async def load_ability(self, request):
        await self.services.get('auth_svc').check_permissions(request)
        ability = dict(await request.json())
        ability_dirs = ['plugins/%s/data/abilities' % p.name.lower() for p in self.services.get('plugin_svc').get_plugins()
                        if os.path.isdir('plugins/%s/data/abilities' % p.name.lower())]
        ability_dirs.append('data/abilities')
        for d in ability_dirs:
            for filename in Path(d).rglob('%s.yml' % ability['ability_id']):
                ability_file = filename.read_text()
                return web.Response(body=ability_file)
        return web.Response(body='No ability file found!')
