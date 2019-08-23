class LogicalPlanner:

    def __init__(self, planning_svc):
        self.planning_svc = planning_svc
        self.agent_svc = planning_svc.get_service('agent_svc')

    async def execute(self, operation, phase):
        for member in operation['host_group']:
            for l in await self.planning_svc.select_links(operation, member, phase):
                l.pop('rewards', [])
                await self.agent_svc.perform_action(l)
        await self.planning_svc.wait_for_phase(operation)
