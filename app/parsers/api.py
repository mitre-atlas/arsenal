import re

from app.objects.secondclass.c_fact import Fact
from app.objects.secondclass.c_relationship import Relationship
from app.utility.base_parser import BaseParser

class Parser(BaseParser):
    """
    Parser that will extract relevant information about an API that has been
        scanned.
        
    Parse Fact store for #{target.api.binding_address} and link facts with found
        API endpoints that contain what is being searched for.
    
    Arguments:
        None
        
    Returns:
        Fact

    """
    def parse(self, blob):
        
        # TODO: include tensorflow::serving
        search_space = ['TorchServe']
        inferenceAPIs = []
        for api in search_space:
            api_lib = re.compile(r'\b{}\b'.format(api), re.IGNORECASE|re.MULTILINE)
            match = re.search(api_lib, blob['metrics']['get']['description'])
            if match is not None:
                inferenceAPIs.append(Relationship(source=Fact(mp.source, api),
                                             edge=mp.edge,
                                             target=Fact(mp.target, None)))
                
        
        
        