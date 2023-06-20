
import pytest

from plugins.arsenal.app.parsers.torchserve_api import Parser


class Mapper():
    def __init__(self, source, edge=None, target=None):
        self.source = source
        self.edge = edge
        self.target = target


@pytest.fixture
def parser():
    parser_info = {
        'mappers': [
            Mapper(source='target.model_server.framework', edge='has_inference_address', target='target.model_server.inference_address'),
            Mapper(source='target.model_server.framework', edge='has_management_address', target='target.model_server.management_address')
        ],
        'used_facts': [],
        'source_facts': []
    }
    torchserve = Parser(
        parser_info=parser_info
    )
    return torchserve


@pytest.fixture
def blob():
    cmd_output = """INFERENCE_API 20.20.20.20:8888
    MANAGEMENT_API 10.10.10.10:9999"""
    return cmd_output


class TestTorchserveAPIParser():
    def test_parse_0(self, parser, blob):
        relationships = parser.parse(blob)

        assert len(relationships) == 2
        assert relationships[0].source.name == 'target.model_server.framework'
        assert relationships[0].source.value == 'TorchServe'
        assert relationships[1].source.name == 'target.model_server.framework'
        assert relationships[1].source.value == 'TorchServe'
        assert relationships[0].target.name == 'target.model_server.inference_address'
        assert relationships[0].target.value == '20.20.20.20:8888'
        assert relationships[1].target.name == 'target.model_server.management_address'
        assert relationships[1].target.value == '10.10.10.10:9999'
