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
        addr_facts = []
        for used_fact in self.used_facts:
            if 'IPv4_address' in used_fact.name:
                addr_facts.append(used_fact.value)
        
        # only allow one IPv4_address fact to be passed to the ability
        # - ie the command (currently) executed within the ability file is:
        # echo #{host.network_interface.IPv4_address} >/dev/null 2>&1 && chmod +x socket_info.sh && ./socket_info.sh
        # - indicates that the parser must be updated if ability command is modified, etc.
        if len(addr_facts) > 1:
            raise NotImplementedError
        
        relationships = []
        # store "list" of binding addresses (but with type == str)
        disc_bind_addrs = ''
        # stores the collected IPv4 address, if available
        collected_addr = addr_facts[0] if len(addr_facts) == 1 else None
        for line in self.line(blob):
            bind_addr = ''
            # parser expects "<Local Address:Port> <Process>"
            sock, proc = line.split()
            # split the <Local Address:Port> into <Local Address> <Port>
            local_addr, port = sock.rsplit(':', 1)
            if port in self.exclude:
                continue
            for mp in self.mappers:
                # only creation of target.api.binding_address fact is supported
                if 'binding_address' not in mp.source:
                    raise NotImplementedError
                # check that addr is a valid (IPv4 or IPv6) address
                try:
                    addr_obj = ip_address(local_addr)
                except ValueError as e:
                    # TODO how to handle the exception?
                    # raise e <-- this will cause parsing to STOP...
                    # server listening on all devs, so use host.network_interface.IPv4_addr
                    if local_addr == "*" and collected_addr:
                        # create fact for the disc binding_address
                        bind_addr = ':'.join([collected_addr, port])
                else: 
                    # perform IPv4 check
                    # NOTE: If IPv6 is allowed, enclose addr in '[' and ']'
                    if addr_obj.version == 4:
                        # loopback ex: localhost, 127.0.0.1
                        if addr_obj.is_loopback:
                            pass
                        # unspecified ex: 0.0.0.0
                        elif addr_obj.is_unspecified and collected_addr:
                            # for now, handle "unspecified" case similar to "*" case
                            # create fact for the disc binding_address
                            bind_addr = ':'.join([collected_addr, port])
                        # FIXME: decide how to handle above conditions
                        # any other conditions to add?
                        else: 
                            # For now, if addr is valid IPv4, use it
                            bind_addr = ':'.join([local_addr, port])
                finally: 
                    # create fact (s) for any disc binding_address
                    if bind_addr:
                        # initialize "list" with first discovered bind_addr, if needed
                        disc_bind_addrs = ', '.join([
                            disc_bind_addrs, bind_addr
                        ]) if disc_bind_addrs else bind_addr
        
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