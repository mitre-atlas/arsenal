from app.objects.secondclass.c_fact import Fact
from app.objects.secondclass.c_relationship import Relationship
from app.utility.base_parser import BaseParser

from ipaddress import ip_address


class Parser(BaseParser):
    """TODO add docstring
    """
    def parse(self, blob):
        relationships = []
        # retrieve collected IPv4 address
        addr_facts = []
        for used_fact in self.used_facts:
            if 'IPv4_address' in used_fact.name:
                addr_facts.append(used_fact.value)

        for line in self.line(blob):
            # parser expects "<Local Address:Port> <Process>"
            sock, proc = line.split()
            # split the <Local Address:Port> into <Local Address> <Port>
            addr, port = sock.rsplit(':', 1)
            for mp in self.mappers:
                bind_addr = []
                # only creation of target.api.binding_address fact is supported
                if 'binding_address' not in mp.source:
                    raise NotImplementedError
                # server listening on all devs, so use host.network_interface.IPv4_addr
                if addr == "*":
                    bind_addr = [':'.join([addr, port]) for addr in addr_facts]
                    continue
                # check that addr is a valid (IPv4) address
                try:
                    addr_obj = ip_address(addr)
                except ValueError as e:
                    # TODO how to handle the exception?
                    # raise e <-- this will cause parsing to STOP...
                    continue
                else: 
                    # perform IPv4 check
                    if addr_obj.version == 4:
                        # loopback ex: localhost, 127.0.0.1
                        if addr_obj.is_loopback:
                            pass
                        # unspecified ex: 0.0.0.0
                        elif addr_obj.is_unspecified:
                            pass
                        # any other conditions to add?
                        # else: 

                        # FIXME: decide how to handle above conditions
                        # For now, if addr is valid IPv4, use it
                        bind_addr = [':'.join([addr, port])]
                
                # create fact (s) for discovered binding_address
                for fact in bind_addr:
                    relationships.append(
                        Relationship(source=Fact(mp.source, fact),
                                     edge=mp.edge,
                                     target=Fact(mp.target, None))
                    )
                    
        return relationships