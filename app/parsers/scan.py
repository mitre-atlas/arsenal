from app.objects.c_relationship import Relationship
from plugins.stockpile.app.parsers.base_parser import BaseParser


class Parser(BaseParser):

    def parse(self, blob):
        relationships = []
        for match in self.line(blob):
            values = match.split(':')
            for mp in self.mappers:
                relationships.append(
                    Relationship(source=(mp.source, values[0]),
                                 edge=mp.edge,
                                 target=(mp.target, values[1]))
                )
        return relationships
