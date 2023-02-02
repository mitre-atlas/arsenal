from app.objects.secondclass.c_fact import Fact
from app.objects.secondclass.c_relationship import Relationship
from app.utility.base_parser import BaseParser


class Parser(BaseParser):
    """
    Parser that will connect the binding address to the prediction endpoint.

    """

    def parse(self, blob):
        relationships = []
        # create different fact mappings, dependent on which TS service is discovered
        # NOTE: when TorchServe (TS) starts, it starts two web services:
        #   - Inference API 
        #   - Management API
        for line in self.line(blob):
            # parser expects api endpoint, <model-name> (ex. 10.X.X.X resnet-18, fasterrcnn)
            bind_addr, model_name = line.split(' ')
            for mp in self.mappers:
                # only creation of target.model_server.framework fact is supported ("source" fact of "Relationship")
                if 'model_server.framework' not in mp.source:
                    raise NotImplementedError
                # use BaseParse.used_facts to get associated inference_api
                if model_name != 'null':
                    pred_endpoint = bind_addr + '/predictions/' + model_name
                    relationships.append(
                        Relationship(source=Fact(mp.source, 'TorchServe'),
                                        edge=mp.edge,
                                        target=Fact(mp.target, pred_endpoint))
                    )
        return relationships