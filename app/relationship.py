class Relationship:

    def __init__(self, source, edge, target):
        self.source = source
        self.edge = edge
        self.target = target

    def get_source(self):
        return self.source

    def get_relationship(self):
        return dict(source=self.source, edge=self.edge, target=self.target)
