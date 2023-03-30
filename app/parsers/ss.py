from app.objects.secondclass.c_fact import Fact
from app.objects.secondclass.c_relationship import Relationship
from app.utility.base_parser import BaseParser

from ipaddress import ip_address


class Parser(BaseParser):
    """
    
    Functionality to parse incoming IPv4 addresses and create Fact Sources
        for binding addresses and associated IPv4 addresses if valid.
        
    Excludes common ports from endpoint discovery.
    
    """
    # specify ports to exclude from API endpoint discovery
    exclude = ['21', '22', '23', '25', '53', '111', '139', '445']
    
    def parse(self, blob):
        # retrieve collected IPv4 address
        address_facts = []
        for used_fact in self.used_facts:
            if 'IPv4_address' in used_fact.name:
                address_facts.append(used_fact.value)
        
        # only allow one IPv4_address fact to be passed to the ability
        if len(address_facts) > 1:
            raise NotImplementedError
        
        relationships = []
        # store "list" of binding addresses (but with type == str)
        disc_binding_addresses = ''
        # stores the collected IPv4 address, if available
        collected_address = address_facts[0] if len(address_facts) == 1 else None
        for line in self.line(blob):
            binding_address = ''
            # parser expects "<Local Address:Port> <Process>"
            sock, _ = line.split()
            # split the <Local Address:Port> into <Local Address> <Port>
            local_address, port = sock.rsplit(':', 1)
            if port in self.exclude:
                continue
            # check that addr is a valid (IPv4 or IPv6) address
            try:
                local_address_obj = ip_address(local_address)
            except:
                local_address_obj = None
                # server listening on all devs, so use host.network_interface.IPv4_addr
                if local_address == "*" and collected_address:
                    # create fact for the disc binding_address
                    binding_address = ':'.join([collected_address, port])
            else: 
                # perform IPv4 check
                # NOTE: If IPv6 is allowed, enclose addr in '[' and ']'
                if local_address_obj and local_address_obj.version == 4:
                    # loopback ex: localhost, 127.0.0.1
                    if local_address_obj.is_loopback:
                        pass
                    # unspecified ex: 0.0.0.0
                    elif local_address_obj.is_unspecified and collected_address:
                        # for now, handle "unspecified" case similar to "*" case
                        # create fact for the disc binding_address
                        binding_address = ':'.join([collected_address, port])
                    # any other conditions to add?
                    else: 
                        # For now, if addr is valid IPv4, use it
                        binding_address = ':'.join([local_address, port])
            finally: 
                # create fact (s) for any disc binding_address
                if binding_address:
                    # initialize "list" with first discovered binding_address, if needed
                    disc_binding_addresses = ', '.join([
                        disc_binding_addresses, binding_address
                    ]) if disc_binding_addresses else binding_address

        # remove the trailing ', '
        disc_binding_addresses = disc_binding_addresses.strip(', ')
        for mp in self.mappers:
            # only creation of target.api.binding_address fact is supported
            if 'binding_address' not in mp.source:
                raise NotImplementedError
            relationships.append(
                Relationship(source=Fact(mp.source, disc_binding_addresses),
                             edge=mp.edge,
                             target=Fact(mp.target, None))
            )     
        return relationships

