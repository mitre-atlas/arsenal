class LogicalPlanner:

    def __init__(self, operation, planning_svc):
        self.operation = operation
        self.planning_svc = planning_svc
        self.agent_svc = planning_svc.get_service('agent_svc')
        self.data_svc = planning_svc.get_service('data_svc')

    async def execute(self, phase):
        operation = (await self.data_svc.explode('operation', dict(id=self.operation['id'])))[0]
        for member in operation['host_group']:
            for l in await self.planning_svc.select_links(operation, member, phase):
                await self.agent_svc.perform_action(l)
