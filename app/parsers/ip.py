from app.objects.secondclass.c_relationship import Relationship
from app.utility.base_parser import BaseParser
from ipaddress import IPv4Address as ip_address


class Parser(BaseParser):

    whitelist_options = {
        'multicast': 'is_multicast',
        'loopback': 'is_loopback',
        'link_local': 'is_link_local',
        'reserved': 'is_reserved',
        'global': 'is_global',
        'unspecified': 'is_unspecified',
        'private': 'is_private',
    }

    def parse(self, blob):
        relationships = []
        for ip in self.ip(blob):
            ip_is_valid = self._is_valid_ip(ip)
            if ip_is_valid:
                for mp in self.mappers:
                    if 'whitelist' in dir(mp):
                        ip = self._whitelist_ip(ip, mp.whitelist)
                    if ip:
                        source = self.set_value(mp.source, ip, self.used_facts)
                        target = self.set_value(mp.target, ip, self.used_facts)
                        relationships.append(
                            Relationship(source=(mp.source, source),
                                         edge=mp.edge,
                                         target=(mp.target, target))
                        )
        return relationships

    @staticmethod
    def _is_valid_ip(raw_ip):
        try:
            ip_address(raw_ip)
        except BaseException:
            return False
        return True

    def _whitelist_ip(self, raw_ip, whitelist):
        ip = ip_address(raw_ip)
        for whitelist_option in self.whitelist_options:
            if whitelist_option not in whitelist:
                if getattr(ip, self.whitelist_options[whitelist_option]):
                    return None
        return raw_ip
