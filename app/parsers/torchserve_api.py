from app.objects.secondclass.c_fact import Fact
from app.objects.secondclass.c_relationship import Relationship
from app.utility.base_parser import BaseParser


class Parser(BaseParser):
    """
    Parser that will extract relevant information about an API that has been
        scanned.
        
    Parse Fact store for #{target.api.binding_address} and link facts with found
        API endpoints that contain what is being searched for.

    """

    def parse(self, blob):
        relationships = []
        # create different fact mappings, dependent on which TS service is discovered
        # NOTE: when TorchServe (TS) starts, it starts two web services:
        #   - Inference API 
        #   - Management API
        for line in self.line(blob):
            # parser expects <api_type> <endpoint_bind_addr> (ex. INFERENCE_API 10.X.Y.Y:8080)
            api_type, bind_addr = line.split()
            for mp in self.mappers:
                # only creation of target.model_server.framework fact is supported ("source" fact of "Relationship")
                if 'model_server.framework' not in mp.source:
                    raise NotImplementedError
                # ensure relationship creation is correct; dependent on the <api_type>
                mp_trg_type = mp.target.split('.').pop().split('_')[0]
                if mp_trg_type in api_type.lower():
                    relationships.append(
                        Relationship(source=Fact(mp.source, 'TorchServe'),
                                     edge=mp.edge,
                                     target=Fact(mp.target, bind_addr))
                    )
        return relationships