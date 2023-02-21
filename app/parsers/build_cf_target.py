from app.objects.secondclass.c_fact import Fact
from app.objects.secondclass.c_relationship import Relationship
from app.utility.base_parser import BaseParser


class Parser(BaseParser):
    """
    Parser that will

    """

    def parse(self, blob):
        relationships = []
        
        for line in self.line(blob):
            for mp in self.mappers:
                    relationships.append(
                        Relationship(source=Fact(mp.source, ),
                                        edge=mp.edge,
                                        target=Fact(mp.target, ))
                    )
        return relationships