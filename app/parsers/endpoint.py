from app.objects.secondclass.c_fact import Fact
from app.objects.secondclass.c_relationship import Relationship
from app.utility.base_parser import BaseParser

import logging

class Parser(BaseParser):
    """
    Parser that will connect the binding address to the prediction endpoint.

    """
    def __init__(self, parser_info):
        super().__init__(parser_info)
        self.logs = logging.getLogger('ENDPOINT')
    
    def parse(self, blob):
        relationships = []
        # retrieve collected endpoint addresses
        endpoint_facts = []
        self.logs.info(self.used_facts)
        for used_fact in self.used_facts:
            log_msg = "fact name: {}".format(used_fact.name)
            self.logs.info(log_msg)
            log_msg = "fact value: {}".format(used_fact.value)
            self.logs.info(log_msg)
            
            if 'inference' in used_fact.name:
                endpoint_facts.append(used_fact.value)
   
        if len(endpoint_facts) > 1:
            raise NotImplementedError
        else:
            inf_bind_addr = endpoint_facts[0]
        
        for line in self.line(blob):
            # parser expects api endpoint, <model-name> (ex. 10.X.X.X resnet-18, fasterrcnn)
            _, model_name = line.split(' ')
            for mp in self.mappers:
                # only creation of target.model_server.framework fact is supported ("source" fact of "Relationship")
                if 'model_server.framework' not in mp.source:
                    raise NotImplementedError
                # use BaseParse.used_facts to get associated inference_api
                if model_name != 'null':
                    pred_endpoint = inf_bind_addr + '/predictions/' + model_name
                    relationships.append(
                        Relationship(source=Fact(mp.source, 'TorchServe'),
                                        edge=mp.edge,
                                        target=Fact(mp.target, pred_endpoint))
                    )
        return relationships