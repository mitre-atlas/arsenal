import json
from datetime import datetime
from urllib.parse import urlparse

from aiohttp import web

from app.utility.base_c2 import BaseC2


class HTTP(BaseC2):

    def __init__(self, services):
        super().__init__(services)
        self.services = services
        self.log = self.add_c2('http', self)

    async def start(self):
        app = self.services.get('app_svc').application
        app.router.add_route('POST', '/ping', self._ping)
        app.router.add_route('POST', '/instructions', self._instructions)
        app.router.add_route('POST', '/results', self._results)

    """ PRIVATE """

    async def _ping(self, request):
        return web.Response(text=self.encode_string('pong'))

    async def _instructions(self, request):
        data = json.loads(self.decode_bytes(await request.read()))
        url = urlparse(data['server'])
        port = '443' if url.scheme == 'https' else 80
        data['server'] = '%s://%s:%s' % (url.scheme, url.hostname, url.port if url.port else port)
        data['c2'] = 'http'
        agent = await self.handle_heartbeat(**data)
        instructions = await self.get_instructions(data['paw'])
        response = dict(sleep=await agent.calculate_sleep(), instructions=instructions)
        return web.Response(text=self.encode_string(json.dumps(response)))

    async def _results(self, request):
        data = json.loads(self.decode_bytes(await request.read()))
        data['time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        status = await self.save_results(data['id'], data['output'], data['status'], data['pid'])
        return web.Response(text=self.encode_string(status))
