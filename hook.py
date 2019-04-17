name = 'Open'
description = 'All open-source abilities, adversaries and files'
address = None
store = 'submodules/open/filestore'


async def initialize(app, services):
    data_svc = services.get('data_svc')
    await data_svc.reload_database(adversaries='submodules/open/adversaries.yml',
                                   abilities='submodules/open/abilities')
