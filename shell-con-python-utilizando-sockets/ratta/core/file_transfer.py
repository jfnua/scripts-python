import time
from socket import timeout
from .cipher import encrypt, decrypt

def send_file(connections, path_file, name_file):
	try:
		for cxn, cons in connections:
			try:
				cxn.send(name_file.encode("utf-8"))
				time.sleep(2)
				f = open(path_file, "rb")
				content = f.read(1024).decode("latin1")
				content = encrypt(content, cons).encode("latin1")
				while content:
					cxn.send(content)
					content = f.read(1024).decode("latin1")
					content = encrypt(content, cons).encode("latin1")
				f.close()
			except Exception as err:
				print(f"ERROR [{cxn}]: {err}\n")
		return 0
	except Exception as err:
		return err


def recv_file(connection, name_file, cons):
	with open(f"saved_files/{name_file}", "wb") as file:
		try:
			line = connection.recv(1024).decode("latin1")
			while b"\x04" not in line:
				line = connection.recv(1024).decode("latin1")
				line = decrypt(line, cons).encode("latin1")
				file.write(line)
		except timeout as err:
			print(f"ERROR: {err}. Try Again!")
			connection.settimeout(0)