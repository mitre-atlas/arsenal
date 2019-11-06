class LogicalPlanner:

    def __init__(self, operation, planning_svc):
        self.operation = operation
        self.planning_svc = planning_svc

    async def execute(self, phase):
        for link in await self.planning_svc.get_links(operation=self.operation, phase=phase):
            await self.operation.apply(link)
