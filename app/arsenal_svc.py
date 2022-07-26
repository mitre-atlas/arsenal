import glob

from shutil import which
from aiohttp_jinja2 import template

from app.utility.base_service import BaseService

class ArsenalService(BaseService):

    def __init__(self, services):
        self.auth_svc = services.get('auth_svc')
        self.file_svc = services.get('file_svc')
        self.data_svc = services.get('data_svc')
        self.contact_svc = services.get('contact_svc')
        self.log = self.add_service('arsenal_svc', self)

    @template('arsenal.html')
    async def splash(self, request):
        return dict()
    #     abilities = await self.services.get('data_svc').locate('abilities')
    #     return(dict(abilities=[a.display for a in abilities]))

    # async def get_abilities(self, request):
    #     abilities = await self.services.get('data_svc').locate('abilities')
    #     return web.json_response(dict(abilities=[a.display for a in abilities]))

    async def dynamically_compile(self, headers):
        name, platform = headers.get('file'), headers.get('platform')
        if which('go') is not None:
            plugin, file_path = await self.file_svc.find_file_path(name)
            output = 'plugins/%s/data/payloads/%s-%s' % (plugin, name, platform)
            await self.file_svc.compile_go(platform, output, file_path)
        return '%s-%s' % (name, platform), '%s-%s' % (name, platform)

    async def load_c2_config(self, directory):
        c2_configs = {}
        for filename in glob.iglob('%s/*.yml' % directory, recursive=False):
            for c2 in self.data_svc.strip_yml(filename):
                c2_configs[c2['name']] = c2
        return c2_configs
