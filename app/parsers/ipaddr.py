from app.objects.secondclass.c_fact import Fact
from app.objects.secondclass.c_relationship import Relationship
from app.utility.base_parser import BaseParser

from ipaddress import ip_address, ip_interface


class Parser(BaseParser):
    """
    Functionality that parses network and IP addresses and stores the pairs as a fact
        if they are valid address.
    
    
    # TODO: remove the '.1' subnet once there is another method to parse dev 'docker0'
    """
    
    exclude = ['0.0.0.0', '127.0.0.1']
    subnet_exclude = ['.255', '.0', '.1']

    def parse(self, blob):
        relationships = []

        # create multiple fact mappings for each network dev-ipaddr pair
        for line in self.line(blob):
            # parser expects "<dev_name> <dev_IPv4_CIDR_range>" (ex: eth0 10.X.Y.Y/16)
            dev, dev_cidr_range = line.split()

            dev_raw_ip = dev_cidr_range
            if "/" in dev_cidr_range:
                dev_raw_ip = dev_raw_ip.split("/")[0]

            if self._is_valid_ip(dev_raw_ip):
                relationships.extend(self._apply_mappers(
                    dev=dev,
                    dev_cidr_range=dev_cidr_range
                ))

        return relationships

    def _apply_mappers(self, dev: str, dev_cidr_range: str):
        relationships = [Relationship(
            source=Fact(mp.source, dev),
            edge=mp.edge,
            target=Fact(mp.target, self.parse_opts[mp.target.split('.').pop()](dev_cidr_range))
        ) for mp in self.mappers]

        return relationships

    @property
    def parse_opts(self):
        return dict(
            IPv4_address=self.parse_ip_address,
            IPv4_network=self.parse_ip_network
        )

    @staticmethod
    def parse_ip_address(dev_cidr_range: str):
        ip_addr = ip_interface(dev_cidr_range).ip
        return str(ip_addr)

    @staticmethod 
    def parse_ip_network(dev_cidr_range: str):
        ip_network = ip_interface(dev_cidr_range).network
        return str(ip_network)

    def _is_valid_ip(self, raw_ip):
        try:
            # The following hardcoded addresses are not used to bind to an interface:
            #   - ['.255', '.0', '.1'] 
            if raw_ip in self.exclude:
                return False
            if any([True if raw_ip.endswith(x) else None for x in self.subnet_exclude]):
                return False
            ip_address(raw_ip)
        except Exception:
            return False
        return True