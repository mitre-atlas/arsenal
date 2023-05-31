from app.objects.secondclass.c_fact import Fact
from app.objects.secondclass.c_relationship import Relationship
from app.utility.base_parser import BaseParser


class Parser(BaseParser):
    """
    Parser that will extract relevant information about an API that has been
        scanned.
    
    Parser expects <api_type> <endpoint_bind_addr> 
        (ex. INFERENCE_API 10.X.Y.Y:<port>)
        
    Parse Fact store for #{target.model_server} and link facts
        with found API endpoints. When TorchServe (TS) starts
        it starts two web services:
           - Inference API 
           - Management API
    """

    def parse(self, blob):
        relationships = []
        for line in self.line(blob):
            api_type, bind_addr = line.split()
            for mp in self.mappers:
                if 'model_server.framework' not in mp.source:
                    raise NotImplementedError('only creation of target.model_server.framework fact is supported')
                target_type = self._map_target_type(mp)
                if target_type in api_type.lower():
                    relationships.append(
                        Relationship(
                            source=Fact(mp.source, 'TorchServe'),
                            edge=mp.edge,
                            target=Fact(mp.target, bind_addr)
                        )
                    )
        return relationships

    def _map_target_type(self, map):
        """
        Funtionality to extract api endpoint type from target
        """
        
        targets = map.target.split('.').pop()
        target_type = targets.split('_')[0]
        
        return target_type
        
        