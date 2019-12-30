from app.utility.base_obfuscator import BaseObfuscator


class Obfuscation(BaseObfuscator):

    def __init__(self, agent):
        self.agent = agent

    def run(self, link):
        return self.decode_bytes(link.command)
