class Relationship:

    def __init__(self, source, edge, target):
        self.source = source
        self.edge = edge
        self.target = target

    def get_source(self):
        return self.source

    def get_target(self):
        return self.target

    def get_edge(self):
        return self.edge
