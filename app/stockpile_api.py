from aiohttp import web
from pathlib import Path


class StockpileApi:

    def __init__(self, services):
        self.services = services

    async def load_ability(self, request):
        await self.services.get('auth_svc').check_permissions(request)
        ability = dict(await request.json())
        for filename in Path('plugins/stockpile/abilities').glob('**/%s.yml' % ability['ability_id']):
            ability_file = filename.read_text()
            return web.Response(body=ability_file)
