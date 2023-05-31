
import pytest

from plugins.arsenal.app.parsers.ss import Parser


class UsedFact():
    def __init__(self, name, value):
        self.name = name
        self.value = value


class Mapper():
    def __init__(self, source, edge=None, target=None):
        self.source = source
        self.edge = edge
        self.target = target


@pytest.fixture
def parser():
    parser_info = {
        'mappers': [Mapper(source='target.api.binding_address_list')],
        'used_facts': [UsedFact('IPv4_address', 'bind_address')],
        'source_facts': []
    }
    ss = Parser(
        parser_info=parser_info
    )
    return ss


@pytest.fixture
def blob():
    cmd_output = """127.0.0.53%lo:53 users:(("systemd-resolve",pid=868,fd=13))
    0.0.0.0:22 users:(("sshd",pid=1611,fd=3))
    127.0.0.1:631 users:(("cupsd",pid=118744,fd=7))
    127.0.0.1:34041 users:(("node",pid=124268,fd=18))
    0.0.0.0:3001 users:(("test",pid=2640,fd=4))
    0.0.0.0:3005 users:(("test",pid=2641,fd=4))
    10.2.4.1:3006 users:(("test",pid=2642,fd=4))
    127.0.0.1:36703 users:(("node",pid=124588,fd=29))
    127.0.0.1:2947 users:(("systemd",pid=1,fd=171))
    [::]:22 users:(("sshd",pid=1611,fd=4))"""
    return cmd_output


class TestSSParser():
    def test_parse_0(self, parser, blob):
        relationships = parser.parse(blob)

        assert len(relationships) == 1
        assert relationships[0].source.name == 'target.api.binding_address_list'
        assert relationships[0].source.value == 'bind_address:3001, bind_address:3005, 10.2.4.1:3006'
