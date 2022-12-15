from ipaddress import ip_address, ip_interface

from app.objects.secondclass.c_fact import Fact
from app.objects.secondclass.c_relationship import Relationship
from app.utility.base_parser import BaseParser


class Parser(BaseParser):
    exclude = ['0.0.0.0', '127.0.0.1']
    # FIXME remove the '.1' subnet once there is another method to parse dev 'docker0'
    subnet_exclude = ['.255', '.0', '.1']

    def parse(self, blob):
        relationships = []
        # create multiple fact mappings for each network dev-ipaddr pair
        for line in self.line(blob):
            # parser expects "<dev_name> <dev_IPv4_CIDR_range>" (ex: eth0 10.X.Y.Y/16)
            dev, dev_cidr_range = line.split()
            # remove the prefixlen, if necessary
            dev_raw_ip = dev_cidr_range
            if "/" in dev_cidr_range:
                dev_raw_ip = dev_cidr_range.split("/")[0]
            # ensure IP is "valid" before storing as a fact
            if self._is_valid_ip(dev_raw_ip):
                for mp in self.mappers:
                    # Proper usage of parser should yield: 
                    #   match == ("IPv4_address" | "IPv4_network")
                    match = self.parse_opts[mp.target.split('.').pop()](dev_cidr_range)
                    relationships.append(Relationship(source=Fact(mp.source, dev),
                                                      edge=mp.edge,
                                                      target=Fact(mp.target, match)))
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