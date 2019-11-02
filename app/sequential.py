class LogicalPlanner:

    def __init__(self, operation, planning_svc):
        self.operation = operation
        self.planning_svc = planning_svc

    async def execute(self, phase):
        for member in self.operation.agents:
            for link in await self.planning_svc.select_links(self.operation, member, phase):
                await self.operation.apply(link)
