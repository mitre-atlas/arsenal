import json
from datetime import datetime
from urllib.parse import urlparse

from aiohttp import web
from app.objects.c_c2 import C2


class HTTP(C2):

    def __init__(self, services, module, config, name):
        super().__init__(services, module, config, name)

    def start(self, app):
        app.router.add_route('POST', '/ping', self._ping)
        app.router.add_route('POST', '/instructions', self._instructions)
        app.router.add_route('POST', '/results', self._results)

    def valid_config(self):
        """
        Overriding of super class function. Always returns True because config is done in code
        :return:
        """
        return True

    """ PRIVATE """

    async def _ping(self, request):
        return web.Response(text=self.encode_string('pong'))

    async def _instructions(self, request):
        data = json.loads(self.decode_bytes(await request.read()))
        url = urlparse(data['server'])
        port = '443' if url.scheme == 'https' else 80
        data['server'] = '%s://%s:%s' % (url.scheme, url.hostname, url.port if url.port else port)
        data['c2'] = self.name
        agent = await self.handle_heartbeat(**data)
        instructions = await self.get_instructions(data['paw'])
        response = dict(sleep=await agent.calculate_sleep(), instructions=instructions)
        return web.Response(text=self.encode_string(json.dumps(response)))

    async def _results(self, request):
        data = json.loads(self.decode_bytes(await request.read()))
        data['time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        status = await self.save_results(data['id'], data['output'], data['status'], data['pid'])
        return web.Response(text=self.encode_string(status))
