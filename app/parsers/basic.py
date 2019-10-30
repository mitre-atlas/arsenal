from plugins.stockpile.app.parsers.base_parser import BaseParser
from plugins.stockpile.app.relationship import Relationship


class Parser(BaseParser):

    def parse(self, blob):
        relationships = []
        for match in self.line(blob):
            for mp in self.mappers:
                source = self.set_value(mp.source, match, self.used_facts)
                target = self.set_value(mp.target, match, self.used_facts)
                relationships.append(
                    Relationship(source=(mp.source, source),
                                 edge=mp.edge,
                                 target=(mp.target, target))
                )
        return relationships
