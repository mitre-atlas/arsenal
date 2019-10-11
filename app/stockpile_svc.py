from shutil import which


class StockpileService:

    def __init__(self, file_svc):
        self.file_svc = file_svc
        self.log = file_svc.add_service('stockpile_svc', self)

    async def dynamically_compile(self, headers):
        name, platform = headers.get('file'), headers.get('platform')
        if which('go') is not None:
            plugin, file_path = await self.file_svc.find_file_path(name)
            output = 'plugins/%s/payloads/%s-%s' % (plugin, name, platform)
            self.log.debug('Dynamically compiling %s' % name)
            await self.file_svc.compile_go(platform, output, file_path)
        return '%s-%s' % (name, platform)
