import json

from aiohttp import web
from datetime import datetime
from urllib.parse import urlparse

from app.interfaces.c2_passive_interface import C2Passive


class HTTP(C2Passive):

    def __init__(self, services, config):
        super().__init__(config=config)
        self.app = services.get('app_svc').application
        self.contact_svc = services.get('contact_svc')

    async def start(self):
        self.app.router.add_route('POST', '/ping', self._ping)
        self.app.router.add_route('POST', '/instructions', self._instructions)
        self.app.router.add_route('POST', '/results', self._results)

    def valid_config(self):
        if hasattr(self.app, 'router'):
            return True
        return False

    """ PRIVATE """

    async def _ping(self, request):
        return web.Response(text=self.contact_svc.encode_string('pong'))

    async def _instructions(self, request):
        data = json.loads(self.contact_svc.decode_bytes(await request.read()))
        url = urlparse(data['server'])
        port = '443' if url.scheme == 'https' else 80
        data['server'] = '%s://%s:%s' % (url.scheme, url.hostname, url.port if url.port else port)
        data['c2'] = 'http'
        agent = await self.contact_svc.handle_heartbeat(**data)
        instructions = await self.contact_svc.get_instructions(data['paw'])
        response = dict(sleep=await agent.calculate_sleep(), instructions=instructions)
        return web.Response(text=self.contact_svc.encode_string(json.dumps(response)))

    async def _results(self, request):
        data = json.loads(self.contact_svc.decode_bytes(await request.read()))
        data['time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        status = await self.contact_svc.save_results(data['id'], data['output'], data['status'], data['pid'])
        return web.Response(text=self.contact_svc.encode_string(status))
