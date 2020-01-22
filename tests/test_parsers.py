import unittest

from app.objects.c_parserconfig import ParserConfig
from plugins.stockpile.app.parsers.bookmarks import Parser
from tests.test_base import TestBase


class TestParsers(TestBase):

    def test_bookmarks(self):
        p = Parser(dict(mappers=[ParserConfig(
            source='host.chrome.bookmark_name',
            edge='resolves_to',
            target='host.chrome.bookmark_url')], used_facts=[])
        )
        with open('plugins/stockpile/tests/data/bookmarks.json', 'r') as bookmarks:
            relationships = p.parse(blob=bookmarks.read())
            self.assertEqual(len(relationships), 6)


if __name__ == '__main__':
    unittest.main()
