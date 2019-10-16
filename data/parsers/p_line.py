from plugins.stockpile.data.parsers.p_base import BaseParser, Relationship


class Parser(BaseParser):

    def __init__(self, relationships):
        self.relationships = relationships

    def parse(self, blob):
        relationships = []
        for r in self.relationships:
            for m in self.line(blob):
                match = Relationship(source=(r.get('source'), m), edge=r.get('edge'), target=(r.get('target'), None))
                relationships.append(match)
        return relationships
