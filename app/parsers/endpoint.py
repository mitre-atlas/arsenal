from app.objects.secondclass.c_fact import Fact
from app.objects.secondclass.c_relationship import Relationship
from app.utility.base_parser import BaseParser


class Parser(BaseParser):
    """
    Parser that will connect the binding address to the prediction endpoint.

    Parser expects a newline-seperated list: resnet-18
                                             fasterrcnn
                                             densenet
    """
    
    def parse(self, blob):

        inference_address = self._get_inference_address()

        relationships = []
        for model_name in self.line(blob):
            
            model_name = model_name.strip()
            if model_name == 'null':
                continue

            for mp in self.mappers:
                if 'prediction_endpoint' not in mp.source:
                    raise NotImplementedError('only creation of target.model_server.framework fact is supported')

                pred_endpoint = inference_address + '/predictions/' + model_name
                relationships.append(
                    Relationship(source=Fact(mp.source, pred_endpoint),
                                 edge=mp.edge,
                                 target=Fact(mp.target, None))
                )
        return relationships

    def _get_inference_address(self) -> str:
        """
        Retrieves IP addresses from facts used in execution of the ability.
        """
        address_facts = [used_fact.value for used_fact in self.used_facts if 'inference' in used_fact.name.split('.')[-1]]

        if len(address_facts) != 1:
            raise NotImplementedError(f"Only allow one inference fact to be passed to the ability: {address_facts}")

        inference_address = address_facts[0] if len(address_facts) == 1 else None

        return inference_address