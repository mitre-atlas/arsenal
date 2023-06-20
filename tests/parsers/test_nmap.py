
import pytest

from plugins.arsenal.app.parsers.nmap import Parser


class Mapper():
    def __init__(self, source, edge=None, target=None):
        self.source = source
        self.edge = edge
        self.target = target


@pytest.fixture
def parser():
    parser_info = {
        'mappers': [
            Mapper(source='target.api.binding_address_list')
        ],
        'used_facts': [],
        'source_facts': []
    }
    nmap = Parser(
        parser_info=parser_info
    )
    return nmap


@pytest.fixture
def blob():
    cmd_output = """Host: 0.0.0.0 ()\tPorts: 22/open/tcp//ssh///, 630/open/tcp//test///, 3005/open/tcp//test///\tIgnored State: closed (997)"""
    return cmd_output


class TestNmapParser():
    def test_parse_0(self, parser, blob):
        relationships = parser.parse(blob)

        assert len(relationships) == 1
        assert relationships[0].source.name == 'target.api.binding_address_list'
        assert relationships[0].source.value == '0.0.0.0:630, 0.0.0.0:3005'
