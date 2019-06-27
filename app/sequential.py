class LogicalPlanner:

    def __init__(self, data_svc, planning_svc):
        self.data_svc = data_svc
        self.planning_svc = planning_svc

    async def execute(self, operation, phase):
        for member in operation['host_group']['agents']:
            agent = await self.data_svc.dao.get('core_agent', dict(id=member['agent_id']))
            for l in await self.planning_svc.select_links(operation, agent[0], phase):
                l.pop('rewards', [])
                await self.data_svc.dao.create('core_chain', l)
            await self.planning_svc.wait_for_phase(operation['id'], agent[0]['id'])
