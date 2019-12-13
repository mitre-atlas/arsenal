import glob

from shutil import which


class StockpileService:

    def __init__(self, services):
        self.file_svc = services.get('file_svc')
        self.data_svc = services.get('data_svc')
        self.contact_svc = services.get('contact_svc')

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
