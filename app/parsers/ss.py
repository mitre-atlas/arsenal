from app.objects.secondclass.c_fact import Fact
from app.objects.secondclass.c_relationship import Relationship
from app.utility.base_parser import BaseParser

from ipaddress import ip_address
# import logging


class Parser(BaseParser):
    """TODO add docstring
    """
    # specify ports to exclude from API endpoint discovery
    exclude = ['21', '22', '23', '25', '53', '139', '445']
    # logger = logging.getLogger('ss_parser')

    def parse(self, blob):
        # self.logger.info("ENTERING PARSER")
        relationships = []
        # store "list" of binding addresses (but with type == str)
        disc_bind_addrs = ''
        # retrieve collected IPv4 address
        addr_facts = []
        for used_fact in self.used_facts:
            if 'IPv4_address' in used_fact.name:
                addr_facts.append(used_fact.value)

        for line in self.line(blob):
            # parser expects "<Local Address:Port> <Process>"
            sock, proc = line.split()
            # split the <Local Address:Port> into <Local Address> <Port>
            local_addr, port = sock.rsplit(':', 1)
            if port in self.exclude:
                continue
            for mp in self.mappers:
                bind_addr_list = []
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
                    if local_addr == "*":
                        # ex: if addr_facts has ['10.X.Y.Z', '172.X.Y.Z'], then
                        # bind_addr == ['10.X.Y.Z:<port>', '172.X.Y.Z:<port>']
                        bind_addr_list = [':'.join([addr, port]) for addr in addr_facts]
                else: 
                    # perform IPv4 check
                    # NOTE: If IPv6 is allowed, enclose addr in '[' and ']'
                    if addr_obj.version == 4:
                        # loopback ex: localhost, 127.0.0.1
                        if addr_obj.is_loopback:
                            pass
                        # unspecified ex: 0.0.0.0
                        elif addr_obj.is_unspecified:
                            # for now, handle "unspecified" case similar to "*" case
                            bind_addr_list = [':'.join([addr, port]) for addr in addr_facts]
                        # FIXME: decide how to handle above conditions
                        # any other conditions to add?
                        else: 
                            # For now, if addr is valid IPv4, use it
                            bind_addr_list = [':'.join([local_addr, port])]
                finally: 
                    # create fact (s) for any disc binding_address
                    if len(bind_addr_list) > 0:
                        for bind_addr in bind_addr_list:
                            # create fact for the disc binding_address
                            if disc_bind_addrs == '':
                                # initialize "list" with first bind_addr
                                disc_bind_addrs = bind_addr
                            else: 
                                disc_bind_addrs = ', '.join([
                                    disc_bind_addrs, bind_addr
                                ])
                    # self.logger.info("current state of disc_bind_addrs: {}", str(disc_bind_addrs))
        
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