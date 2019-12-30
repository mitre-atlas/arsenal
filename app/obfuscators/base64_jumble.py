import random
import string

from app.utility.base_world import BaseWorld


class Obfuscation(BaseWorld):

    def __init__(self, agent):
        self.agent = agent

    def run(self, link):
        cmd, extra = self._jumble_command(link.command)
        if self.agent.platform == 'windows':
            return self.decode_bytes(cmd)
        return self.bash(cmd, extra)

    @staticmethod
    def bash(code, extra):
        return 'eval "$(echo %s | rev | cut -c%s- | rev | base64 --decode)"' % (str(code.encode(), 'utf-8'), extra+1)

    """ PRIVATE """

    def _jumble_command(self, s):
        extra = 0
        while self.is_base64(s):
            s = s + self._random_char()
            extra += 1
        return s, extra

    @staticmethod
    def _random_char():
        return random.choice(string.ascii_letters + string.digits)
