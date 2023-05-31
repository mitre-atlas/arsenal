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
        
        collected_address = self._get_collected_address()
        binding_addresses = self._parse_to_binding_addresses(blob, collected_address)

        relationships = []
        for mp in self.mappers:
            if 'binding_address' not in mp.source:
                raise NotImplementedError('only creation of target.api.binding_address fact is supported')
            relationships.append(
                Relationship(
                    source=Fact(mp.source, binding_addresses),
                    edge=mp.edge,
                    target=Fact(mp.target, None)
                )
            )     
        return relationships

    def _get_collected_address(self) -> str:
        """
        Retrieves IP addresses from facts used in execution of the ability.
        """
        address_facts = [used_fact.value for used_fact in self.used_facts if 'IPv4_address' in used_fact.name]

        if len(address_facts) > 1:
            raise NotImplementedError(f"Only allow one IPv4_address fact to be passed to the ability: {address_facts}")

        collected_address = address_facts[0] if len(address_facts) == 1 else None

        return collected_address

    def _parse_to_binding_addresses(self, blob: str, collected_address: str) -> str:
        """
        Main parsing method. Turns the text blob into a single string containing binding addresses.
        """
        disc_binding_addresses = ''
        for line in self.line(blob):

            sock, _ = line.split()  # parser expects "<Local Address:Port> <Process>"
            local_address, port = sock.rsplit(':', 1)   # split the <Local Address:Port> into <Local Address> <Port>
            if port in self.exclude:
                continue

            bind_address = None

            try:
                local_address_obj = ip_address(local_address)
            except:
                local_address_obj = None

            if local_address_obj and local_address_obj.version == 4 and not local_address_obj.is_loopback:
                if local_address_obj.is_unspecified:
                    bind_address = collected_address
                else:
                    bind_address = local_address
            elif local_address_obj is None:
                if local_address == '*':
                    bind_address = collected_address

            if bind_address is not None:
                bind_address = ':'.join([bind_address, port])
                disc_binding_addresses = ', '.join([
                    disc_binding_addresses, bind_address
                ]) if disc_binding_addresses else bind_address

        disc_binding_addresses = disc_binding_addresses.strip(', ')
        return disc_binding_addresses