from plugins.stockpile.app.parsers.base_parser import BaseParser
from plugins.stockpile.app.relationship import Relationship


class Parser(BaseParser):

    def __init__(self, parser_info):
        self.mappers = parser_info['mappers']
        self.used_facts = parser_info['used_facts']

    def parse(self, blob):
        relationships = []
        for match in self.line(blob):
            for mp in self.mappers:
                source = self.set_value(mp.get('source'), match, self.used_facts)
                target = self.set_value(mp.get('target'), match, self.used_facts)
                relationships.append(
                    Relationship(source=(mp.get('source'), source),
                                 edge=mp.get('edge'),
                                 target=(mp.get('target'), target))
                )
        return relationships
