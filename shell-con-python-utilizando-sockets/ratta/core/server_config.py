from socket import *
from random import randint
from time import sleep
from .cipher import generate_key, generate_int, encrypt


class ConnectionSocket(socket):

    def __init__(self, host, port):
        super().__init__()
        self.__host = host
        self.__port = port
        self.__targetList = {}  # contains all hosts
        self.__blockList = []
        self._idTargetList = 1  #ID only is created for user manipulated easy IPs.
        self._idBlockList = 1

    def create_socket(self):
        try:
            gethostbyname(self.__host)
            s = socket(AF_INET, SOCK_STREAM)
            s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            s.bind((self.__host, int(self.__port)))
            s.listen(10)
            return s
        
        except gaierror:
            print("\n[-] Host not Found")
            return 1
        except ValueError:
            print("\n[-] Port not Found!\n")
            return 1

    def activate_socket(self, s):
        try:
            while True:
                c, addr = s.accept()

                refuse = self.__refused(addr[0])

                if refuse:
                    c.close()
                else:
                    try:
                        c.settimeout(3)   #established connection with settimeout in 3 sec, if not response, append to blocklist or refused
                        os, encrypt = c.recv(1024).decode("utf-8").split("-")  # It receives: OS, int (int>0 Encrypt, other plaintext)
                        key = None
                        const = 0
                        if int(encrypt) > 0:
                            pass
                            #cons = self.diffie_hellman(c)

                        self.__targetList[addr[0]] = [addr[1], c, key, const, os, self._idTargetList]
                        self._idTargetList += 1

                    except timeout:
                        c.close()
                sleep(0.05)

        except Exception:
            print("[-] Server stopped")

    def __refused(self, ip):
        block = False
        for host in self.__blockList:
            if ip == host[1]:
                block = True
        return block
    """
    def exchange_keys(self, cxn):
        key_public = generate_key()
        int_for_keypublic = generate 
	key_private = generate_key()
       """ 
    def diffie_hellman(self, cxn):
        p = generate_int(randint(5,10))*2+1
        k = generate_int(randint(2,4))
        x = generate_int(randint(2,4))
        print(x)
        A = k**x%p
        cxn.send(f"{str(p)}\x03{str(k)}\x03{str(A)}".encode())
        B = int(cxn.recv(512).decode())
        return B**x%p

    @property
    def show_current_server(self):
        return [self.__host, self.__port]

    @property
    def show_hostList(self):
        return self.__targetList

    @property
    def show_blockList(self):
        return self.__blockList

    def add_blockList(self, hosts):
        adds = []
        if isinstance(hosts[0],str):
            for host in hosts:
                if host in self.__targetList:
                    self.__targetList[host][1].close()
                    self.__blockList.append((self._idBlockList, host))
                    adds.append(host)
        else:
            for ID in hosts:
                for host in self.__targetList:
                    if ID == self.__targetList[host][4]:
                        self.__targetList[host][1].close()
                        self.__blockList.append((self._idBlockList, host))
                        adds.append(host)
        for host in adds:
            del self.__targetList[host]
        self._idBlockList += 1

    def remove_blockList(self, hosts):
        for host in hosts:
            for n, address in self.__blockList:
                if host == n or host == address:
                    self.__blockList.remove((n, address))

    def close_socket(self, s):
        if self.__targetList:
            for address in self.__targetList:
                self.__targetList[address][1].close()
        del self.__targetList
        del self.__blockList
        s.close()

    def block_all(self):
        self.add_blockList([address for address in self.__targetList])

    def free_all(self):
        self.remove_blockList([host for _, host in self.__blockList])

