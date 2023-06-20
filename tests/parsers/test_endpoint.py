
import pytest

from plugins.arsenal.app.parsers.endpoint import Parser


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
        'mappers': [
            Mapper(source='target.model_server.prediction_endpoint')
        ],
        'used_facts': [UsedFact('target.model_server.inference_address', 'bind_address')],
        'source_facts': []
    }
    endpoint = Parser(
        parser_info=parser_info
    )
    return endpoint


@pytest.fixture
def blob():
    cmd_output = """resnet-18
    other-model"""
    return cmd_output


class TestEndpointParser():
    def test_parse_0(self, parser, blob):
        relationships = parser.parse(blob)

        assert len(relationships) == 2
        assert relationships[0].source.name == 'target.model_server.prediction_endpoint'
        assert relationships[0].source.value == 'bind_address/predictions/resnet-18'
        assert relationships[1].source.name == 'target.model_server.prediction_endpoint'
        assert relationships[1].source.value == 'bind_address/predictions/other-model'