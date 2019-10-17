from plugins.stockpile.app.parsers.base_parser import BaseParser, Relationship


class Parser(BaseParser):

    def __init__(self, parser_info):
        self.mappers = parser_info['mappers']
        self.used_facts = parser_info['used_facts']

    def parse(self, blob):
        relationships = []
        for mp in self.mappers:
            for match in self.line(blob):
                relationships.append(
                    Relationship(source=(mp.get('source'), self.set_value(mp.get('source'), match, self.used_facts)),
                                 edge=mp.get('edge'),
                                 target=(mp.get('target'), self.set_value(mp.get('target'), match, self.used_facts)))
                )
        return relationships

