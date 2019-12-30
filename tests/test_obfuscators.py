import unittest

from app.objects.c_ability import Ability
from app.objects.c_agent import Agent
from app.objects.c_link import Link
from app.objects.c_obfuscator import Obfuscator
from tests.test_base import TestBase


class TestObfuscators(TestBase):

    def setUp(self):
        self.command = 'd2hvYW1p'
        dummy_ability = Ability(ability_id=None, tactic=None, technique_id=None, technique=None, name=None, test=None,
                                description=None, cleanup=None, executor='sh', platform=None, payload=None,
                                parsers=None, requirements=None, privilege=None)
        self.dummy_agent = Agent(paw='123', platform='linux', executors=['sh'])
        self.dummy_link = Link(operation=None, command=self.command, paw='123', ability=dummy_ability)

    def test_plain_text(self):
        o = Obfuscator(name='plain-text', module='plugins.stockpile.app.obfuscators.plain_text')
        mod = o.load(self.dummy_agent)
        obfuscated_command = mod.run(self.dummy_link)
        self.assertEqual('whoami', obfuscated_command)

    def test_base64_basic(self):
        o = Obfuscator(name='base64basic', module='plugins.stockpile.app.obfuscators.base64_basic')
        mod = o.load(self.dummy_agent)
        obfuscated_command = mod.run(self.dummy_link)
        self.assertEqual('eval "$(echo %s | base64 --decode)"' % self.command, obfuscated_command)

    def test_base64_jumble(self):
        o = Obfuscator(name='base64jumble', module='plugins.stockpile.app.obfuscators.base64_jumble')
        mod = o.load(self.dummy_agent)
        obfuscated_command = mod.run(self.dummy_link)
        actual_cmd = obfuscated_command.split()[2]
        self.assertEqual(len(self.command)+1, len(actual_cmd))


if __name__ == '__main__':
    unittest.main()
