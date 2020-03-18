import re
import unittest
from base64 import b64encode
from random import seed

from app.objects.c_agent import Agent
from app.objects.secondclass.c_link import Link
from app.objects.c_ability import Ability
from app.obfuscators.base64_basic import Obfuscation as Base64Obfuscator
from app.obfuscators.plain_text import Obfuscation as PlainTextObfuscator
from app.obfuscators.base64_jumble import Obfuscation as Base64JumbleObfuscator
from app.obfuscators.caesar_cipher import Obfuscation as CaesarCipherObfuscator


class TestObfuscators(unittest.TestCase):

    def setUp(self):
        # for those that are curious -- when abilities are created, commands are b64 encoded
        # by default.
        self.command = 'whoami'
        self.encoded_command = b64encode(self.command.strip().encode('utf-8')).decode()
        self.dummy_ability = Ability(ability_id=None, tactic=None, technique_id=None, technique=None, name=None,
                                     test=None, description=None, cleanup=None, executor='sh', platform=None,
                                     payload=None, variations=[], parsers=None, requirements=None, privilege=None)
        self.dummy_agent = Agent(paw='123', platform='linux', executors=['sh'], server='http://localhost:8888',
                                 sleep_min=0, sleep_max=0, watchdog=0)
        self.dummy_link = Link(id='abc', operation='123', command=self.encoded_command, paw='123',
                               ability=self.dummy_ability)

    def test_plain_text(self):
        o = PlainTextObfuscator(self.dummy_agent)
        obfuscated_command = o.run(self.dummy_link)
        self.assertEqual(self.command, obfuscated_command)

    def test_base64_basic(self):
        o = Base64Obfuscator(self.dummy_agent)
        obfuscated_command = o.run(self.dummy_link)
        # string 'd2hvYW1p' is the base64 encoded value of the string 'whoami'
        self.assertEqual('eval "$(echo %s | base64 --decode)"' % self.encoded_command, obfuscated_command)

    def test_base64_jumble(self):
        o = Base64JumbleObfuscator(self.dummy_agent)
        obfuscated_command = o.run(self.dummy_link)
        # create a regex to test that the command comes back as we expect it, it should have
        # the base64 value, plus only 1 char, so d2hvYW1p. should match that pattern
        expected_command_regex = 'eval "\\$\\(echo d2hvYW1p.| rev | cut -c1- | rev | base64 --decode\\)"'
        self.assertIsNotNone(re.match(expected_command_regex, obfuscated_command))

    def test_caesar_cipher(self):
        seed(1)
        self.dummy_ability.executor = 'psh'
        self.dummy_agent.platform = 'windows'
        self.dummy_agent.executors[0] = 'psh'

        o = CaesarCipherObfuscator(self.dummy_agent)
        obfuscated_command = o.run(self.dummy_link)
        actual_cmd = obfuscated_command.split()[2][1:-2]
        self.assertEqual(len(self.command), len(actual_cmd))


if __name__ == '__main__':
    unittest.main()
