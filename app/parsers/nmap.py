from app.objects.secondclass.c_fact import Fact
from app.objects.secondclass.c_relationship import Relationship
from app.utility.base_parser import BaseParser

import re


class Parser(BaseParser):
    """
    Functionality to parse incoming IPv4 addresses and create Fact Sources
        for binding addresses and associated IPv4 addresses if valid.
        
    Excludes common ports from endpoint discovery.
    """
    exclude = ['21', '22', '23', '25', '53', '111', '139', '445']

    def parse(self, blob):
        
        disc_bind_addrs = self._parse_to_binding_addresses(blob)

        relationships = []
        for mp in self.mappers:
            if 'binding_address' not in mp.source:
                raise NotImplementedError('only creation of target.api.binding_address fact is supported')
            relationships.append(
                Relationship(source=Fact(mp.source, disc_bind_addrs),
                             edge=mp.edge,
                             target=Fact(mp.target, None))
            )     
        return relationships

    def _parse_to_binding_addresses(self, blob):
        disc_bind_addrs = ''
        for line in self.line(blob):
            host_data, ports_data = line.split('\t')[:2]

            host_ip_addr = self.ip(host_data)[0]
            ports_data = ports_data.strip('Ports: ')
            if len(ports_data) == 0:
                continue

            for port_info in ports_data.split():
                port, state = re.split('/{1,3}', port_info)[:-3]
                
                if port in self.exclude or state != 'open':
                    continue

                bind_addr = ':'.join([host_ip_addr, port])

                disc_bind_addrs = ', '.join([
                    disc_bind_addrs, bind_addr
                ]) if disc_bind_addrs else bind_addr

        disc_bind_addrs = disc_bind_addrs.strip(', ')

        return disc_bind_addrs