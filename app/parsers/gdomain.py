from app.objects.c_relationship import Relationship
from plugins.stockpile.app.parsers.base_parser import BaseParser
from app.utility.logger import Logger


class Parser(BaseParser):

    def __init__(self, parser_info):
        super().__init__(parser_info)
        self.mappers = parser_info['mappers']
        self.used_facts = parser_info['used_facts']
        self.log = Logger('Parser')

    def gd_parser(self, text):
        results = dict()

        for block in text.split('\r\n\r\n'):
            if block:
                hostname = None
                pvi = None
                for line in block.splitlines():
                    hostname = self._parse_hostname(line, hostname)
                    pvi = self._parse_version(line, pvi)
                    if line.startswith('Exception') and '(0x80005000)' in line:
                        # Domain communication error
                        self.log.warning('Get-Domain parser: Domain Issue 0x80005000: Verify that the rat is running '
                                         'under a Domain Account, and that the Domain Controller can be reached.')
                if hostname and pvi:
                    results[hostname] = dict(parsed_version_info=pvi)
        if not results:
            self.log.warning('Get-Domain Parser: Returned data contained no parseable information!')
        return results

    def parse(self, blob):
        relationships = []
        try:
            parse_data = self.gd_parser(blob)
            for match in parse_data:
                for mp in self.mappers:
                    relationships.append(
                        Relationship(source=(mp.source, match),
                                     edge=mp.edge,
                                     target=(mp.target, None)))
        except Exception as error:
            self.log.warning('Get-Domain parser encountered an error - {}. Continuing...'.format(error))
        return relationships

    '''    PRIVATE FUNCTION     '''

    @staticmethod
    def _parse_hostname(line, current):
        if line.startswith('dnshostname'):
            field_name, value = [c.strip() for c in line.split(':')]
            return value.lower()
        return current

    @staticmethod
    def _parse_version(line, current):
        if line.startswith('operatingsystemversion'):
            value = line.split(':')[-1].strip()  # Looks like: '10.0 (14393)'
            os_version, build_number = value.split(' ')
            build_number = build_number[1:-1]  # remove parens
            major_version, minor_version = os_version.split('.')
            return dict(os_name='windows', major_version=major_version,
                        minor_version=minor_version, build_number=build_number)
        return current
