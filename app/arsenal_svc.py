
import os

from aiohttp_jinja2 import template

from app.utility.base_service import BaseService


class ArsenalService(BaseService):

    def __init__(self, services):
        self.auth_svc = services.get('auth_svc')
        self.file_svc = services.get('file_svc')
        self.data_svc = services.get('data_svc')
        self.contact_svc = services.get('contact_svc')
        self.log = self.add_service('arsenal_svc', self)
        self.arsenal_dir = os.path.join('plugins', 'arsenal')

    @template('arsenal.html')
    async def splash(self, request):
        return dict()
