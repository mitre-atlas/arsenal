name = 'Open'
description = 'All open-source abilities, adversaries and files'
address = None
store = 'plugins/open/filestore'


async def initialize(app, services):
    data_svc = services.get('data_svc')
    await data_svc.reload_database(adversaries='plugins/open/adversaries.yml',
                                   abilities='plugins/open/abilities')
