
from app.objects.secondclass.c_fact import Fact
from app.objects.secondclass.c_relationship import Relationship
from app.utility.base_parser import BaseParser

class Parser(BaseParser):
    """
    Parser that will extract relevant information about an API that has been
        scanned.
        
    Parse Fact store for #{target.api.binding_address} and link facts with found
        API endpoints that contain what is being searched for.
        
    NOTE: regexs pre-defined.

    Arguments:
        None
        
    Returns:
        Fact

    """
    def parse(self, blob):
        relationships = []
        for line in self.line(blob):
            # split line for API and IP
            endpoint, ip = line.split(' ')
            for mp in self.mappers:
                relationships.append(
                    Relationship(source=Fact(mp.source, endpoint),
                                edge=ip,
                                target=Fact(mp.target, None))
                )
        return relationships

        