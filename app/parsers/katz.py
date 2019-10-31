from plugins.stockpile.app.parsers.base_parser import BaseParser
from plugins.stockpile.app.relationship import Relationship
from app.utility.logger import Logger

import re
from collections import defaultdict


class MimikatzBlock(object):
    def __init__(self):
        self.session = ''
        self.username = ''
        self.domain = ''
        self.logon_server = ''
        self.logon_time = ''
        self.sid = ''
        self.packages = defaultdict(list)


class Parser(BaseParser):

    def __init__(self, parser_info):
        self.mappers = parser_info['mappers']
        self.used_facts = parser_info['used_facts']
        self.parse_mode = 'wdigest'
        self.log = Logger('parsing_svc')

    def parse_katz(self, output):
        """
        Parses mimikatz output with the logonpasswords command and returns a list of dicts of the credentials.
        Args:
            output: stdout of "mimikatz.exe privilege::debug sekurlsa::logonpasswords exit"
        Returns:
            A list of MimikatzSection objects
        """
        sections = output.split('Authentication Id')  # split sections using "Authentication Id" as separator
        creds = []
        for section in sections:
            mk_section = MimikatzBlock()
            package = {}
            package_name = ''
            in_header = True
            pstate = False
            for line in section.splitlines():
                line = line.strip()
                if in_header:
                    in_header = self._parse_header(line, mk_section)
                    if in_header:
                        continue  # avoid excess parsing work
                pstate, package_name = self._process_package(line, package, package_name, mk_section)
                if pstate:
                    pstate = False
                    package = {}
            self._package_extend(package, package_name, mk_section)  # save the current ssp if necessary
            if mk_section.packages:  # save this section
                creds.append(mk_section)
        return creds

    def parse(self, blob):
        relationships = []
        try:
            parse_data = self.parse_katz(blob)
            for match in parse_data:
                if self.parse_mode in match.packages:
                    for mp in self.mappers:
                        relationships.append(
                            Relationship(source=(mp.source, match.packages[self.parse_mode][0]['Username']),
                                         edge=mp.edge,
                                         target=(mp.target, match.packages[self.parse_mode][0]['Password']))
                        )
        except Exception as error:
            self.log.warning('Mimikatz parser encountered an error - {}. Continuing...'.format(error))
        return relationships

    """    PRIVATE FUNCTION     """

    @staticmethod
    def _parse_header(line, mk_section):
        if line.startswith('msv'):
            return False
        session = re.match(r'^\s*Session\s*:\s*([^\r\n]*)', line)
        if session:
            mk_section.session = session.group(1)
        username = re.match(r'^\s*User Name\s*:\s*([^\r\n]*)', line)
        if username:
            mk_section.username = username.group(1)
        domain = re.match(r'^\s*Domain\s*:\s*([^\r\n]*)', line)
        if domain:
            mk_section.domain = domain.group(1)
        logon_server = re.match(r'^\s*Logon Server\s*:\s*([^\r\n]*)', line)
        if logon_server:
            mk_section.logon_server = logon_server.group(1)
        logon_time = re.match(r'^\s*Logon Time\s*:\s*([^\r\n]*)', line)
        if logon_time:
            mk_section.logon_time = logon_time.group(1)
        sid = re.match(r'^\s*SID\s*:\s*([^\r\n]*)', line)
        if sid:
            mk_section.sid = sid.group(1)
        return True

    def _process_package(self, line, package, package_name, mk_section):
        if line.startswith('['):
            self._package_extend(package, package_name, mk_section)  # this might indicate the start of a new account
            return True, package_name  # reset the package
        elif line.startswith('*'):
            m = re.match(r'\s*\* (.*?)\s*: (.*)', line)
            if m:
                package[m.group(1)] = m.group(2)
        elif line:
            match_group = re.match(r'([a-z]+) :', line)  # parse out the new section name
            if match_group:  # this is the start of a new ssp
                self._package_extend(package, package_name, mk_section)  # save the current ssp if necessary
                return True, match_group.group(1)  # reset the package
        return False, package_name

    @staticmethod
    def _package_extend(package, package_name, mk_section):
        if 'Username' in package and package['Username'] != '(null)' and \
                (('Password' in package and package['Password'] != '(null)') or 'NTLM' in package):
            mk_section.packages[package_name].append(package)
