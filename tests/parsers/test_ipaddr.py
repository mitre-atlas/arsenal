
import pytest

from plugins.arsenal.app.parsers.ipaddr import Parser


class Mapper():
    def __init__(self, source, edge=None, target=None):
        self.source = source
        self.edge = edge
        self.target = target


@pytest.fixture
def parser():
    parser_info = {
        'mappers': [
            Mapper(source='host.network_interface.name', edge='has_IPv4_address', target='host.network_interface.IPv4_address'),
            Mapper(source='host.network_interface.name', edge='has_IPv4_network', target='host.network_interface.IPv4_network')
        ],
        'used_facts': [],
        'source_facts': []
    }
    ss = Parser(
        parser_info=parser_info
    )
    return ss


@pytest.fixture
def blob():
    cmd_output = """lo 127.0.0.1/8
    interface0 10.0.0.62/24
    interface1 172.0.0.1/16"""
    return cmd_output


class TestIPAddrParser():
    def test_parse_0(self, parser, blob):
        relationships = parser.parse(blob)

        print(relationships[1].source.value)
        print(relationships[1].target.value)

        assert len(relationships) == 2
        assert relationships[0].source.name == 'host.network_interface.name'
        assert relationships[0].source.value == 'interface0'
        assert relationships[1].source.name == 'host.network_interface.name'
        assert relationships[1].source.value == 'interface0'
        assert relationships[0].target.name == 'host.network_interface.IPv4_address'
        assert relationships[0].target.value == '10.0.0.62'
        assert relationships[1].target.name == 'host.network_interface.IPv4_network'
        assert relationships[1].target.value == '10.0.0.0/24'
