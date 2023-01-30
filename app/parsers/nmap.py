from app.objects.secondclass.c_fact import Fact
from app.objects.secondclass.c_relationship import Relationship
from app.utility.base_parser import BaseParser

import re

class Parser(BaseParser):
    # specify ports to exclude from API endpoint discovery
    exclude = ['21', '22', '23', '25', '53', '139', '445']

    def parse(self, blob):
        # parser expects output to be in Nmap's so-called "grepable format" !!
        relationships = []
        # store "list" of binding addresses (but with type == str)
        disc_bind_addrs = ''
        for line in self.line(blob):
            # "Host" info displayed 1st and "Ports" info displayed 2nd
            host_data, ports_data = line.split('\t')[:2]
            # retrieve IPv4 address for the remote host (1 addr per line)
            host_ip_addr = self.ip(host_data)[0]
            # remove the title ("indicator") from the "Ports" displayed info
            ports_data = ports_data.strip('Ports: ')
            # ensure that "Ports" info is valid to filter (ie nonempty)
            if len(ports_data) > 0:
                # filter the displayed "Ports" info
                for port_info in ports_data.split():
                    # omitting last element of the split list is intentional !!
                    # example output of "re.split('/{1,3}', port_info)"
                    #   - ['8080', 'open', 'tcp', 'http-proxy', '']
                    port_info = re.split('/{1,3}', port_info)[:-1]
                    # assume that len(port_info) == 4; else, incorrect usage of parser
                    # NOTE: proto and svc are NOT used (currently) to create any facts
                    port, state, proto, svc = port_info
                    
                    if port in self.exclude:
                        continue
                    # only use port_info for ports with STATE == "open" 
                    # NOTE: there are six "port states" recognized by Nmap
                    #   - see https://nmap.org/book/man-port-scanning-basics.html
                    if state == 'open':
                        bind_addr = ':'.join([host_ip_addr, port])
                        # create fact (s) for any disc binding_address
                        if bind_addr:
                            # initialize "list" with first discovered bind_addr, if needed
                            disc_bind_addrs = ', '.join([
                                disc_bind_addrs, bind_addr
                            ]) if disc_bind_addrs else bind_addr
                        for mp in self.mappers:
                            # only creation of target.api.binding_address fact is supported
                            if 'binding_address' not in mp.source:
                                raise NotImplementedError
        
        # remove the trailing ', '
        disc_bind_addrs = disc_bind_addrs.strip(', ')
        for mp in self.mappers:
            # only creation of target.api.binding_address fact is supported
            if 'binding_address' not in mp.source:
                raise NotImplementedError
            relationships.append(
                Relationship(source=Fact(mp.source, disc_bind_addrs),
                             edge=mp.edge,
                             target=Fact(mp.target, None))
            )     
        return relationships