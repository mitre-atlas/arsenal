import asyncio
import re
from base64 import b64decode, b64encode
from datetime import datetime


class LogicalPlanner:

    def __init__(self, data_svc, log):
        self.data_svc = data_svc
        self.log = log
        self.loop = asyncio.get_event_loop()

    async def execute(self, operation, phase):
        for member in operation['host_group']['agents']:
            agent = await self.data_svc.dao.get('atomic_agent', dict(id=member['agent_id']))
            await self._exhaust_agent(agent[0], operation, phase)

    async def _exhaust_agent(self, agent, operation, phase):
        while True:
            operation = await self.wait_for_agent(operation['id'], agent['id'])
            link = await self.choose_next_link(operation, agent, phase)
            if not link:
                break
            await self.data_svc.dao.create('atomic_chain', link)

    @staticmethod
    async def choose_next_link(operation, agent, phase):
        host_already_ran = [l['command'] for l in operation['chain'] if l['host_id'] == agent['id'] and l['collect']]
        phase_abilities = [i for p, v in operation['adversary']['phases'].items() if p <= phase for i in v]
        for a in phase_abilities:
            decoded_test = b64decode(a['test']).decode('utf-8')
            decoded_test = decoded_test.replace('#{server}', agent['server'])
            decoded_test = decoded_test.replace('#{group}', operation['host_group']['name'])
            encoded_test = str(b64encode(decoded_test.encode()), 'utf-8')
            variables = re.findall(r'#{(.*?)}', decoded_test, flags=re.DOTALL)
            if encoded_test not in host_already_ran and not variables:
                return dict(op_id=operation['id'], host_id=agent['id'], ability_id=a['id'], decide=datetime.now(),
                            command=encoded_test, score=0)

    async def wait_for_agent(self, op_id, agent_id):
        op = await self.data_svc.explode_operation(dict(id=op_id))
        while await self._uncollected_links(op[0], agent_id):
            await asyncio.sleep(3)
            op = await self.data_svc.explode_operation(dict(id=op_id))
        return op[0]

    @staticmethod
    async def _uncollected_links(operation, agent_id):
        return next((lnk for lnk in operation['chain'] if lnk['host_id'] == agent_id and not lnk['finish']), False)
