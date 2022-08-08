import asyncio

class LogicalPlanner:

    def __init__(self, operation, planning_svc, stopping_conditions=()):
        self.operation = operation
        self.planning_svc = planning_svc
        self.stopping_conditions = stopping_conditions
        self.stopping_condition_met = False
        self.state_machine = ['reconnaissance','resource_development', 'ml_model_access', 'initial_access', 'collection', 
                                'ml_model_staging', 'impact', 'execution', 'persistence', 'defence_evasion', 
                                'discovery', 'exfiltration']
        self.next_bucket = 'initial_access'   # set first, bucket to execute
        self.current_length = 0

    async def execute(self):
        await self.planning_svc.execute_planner(self)

    async def do_bucket(self, bucket):
        await self.planning_svc.exhaust_bucket(self, bucket, self.operation)

    async def reconnaissance(self):
        await self.do_bucket('reconnaissance')
        self.next_bucket = await self.planning_svc.default_next_bucket('reconnaissance', self.state_machine)

    async def resource_development(self):
        await self.do_bucket('resource-development')
        self.next_bucket = await self.planning_svc.default_next_bucket('resource_development', self.state_machine)

    async def ml_model_access(self):
        await self.do_bucket('resource-development')
        self.next_bucket = await self.planning_svc.default_next_bucket('resource_development', self.state_machine)

    async def initial_access(self):
        await self.do_bucket('ml-model-access')
        self.next_bucket = await self.planning_svc.default_next_bucket('ml_model_access', self.state_machine)

    async def ml_model_staging(self):
        await self.do_bucket('ml-model-staging')
        self.next_bucket = await self.planning_svc.default_next_bucket('ml-model-staging', self.state_machine)

    async def collection(self):
        await self.do_bucket('collection')
        self.next_bucket = await self.planning_svc.default_next_bucket('collection', self.state_machine)

    async def impact(self):
        await self.do_bucket('impact')
        if len(self.operation.chain) == self.current_length:  # check to see if we've done anything new recently
            if self.operation.auto_close:  # we aren't making any further forward progress, and we should close
                self.next_bucket = None
            else:  # we aren't making any further forward progress, but let's wait a bit and see if that changes
                await asyncio.sleep(180)  # Sleep for a while before we enter the flow loop again
                self.planning_svc.log.debug('[buckets] Ran out of things to do for the moment. Sleeping for a bit.')
                self.next_bucket = 'initial_access'
        else:
            self.current_length = len(self.operation.chain)
            self.next_bucket = await self.planning_svc.default_next_bucket('impact', self.state_machine)
