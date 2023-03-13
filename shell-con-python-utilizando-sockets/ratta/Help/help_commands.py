
"""The command help is '?' """
command_help = """
savefile [namefile]                                      - Save the indicated file in the current path.
sendfile [filepath] ["newFileName (includes extension)"] - Send a file to the target.
block [host or hostlist]                                 - Blocks connections from indicated hosts.
free [host or hostlist]                                  - Releases connections from the indicated hosts.
hosts                                                    - Shows available and blocked hosts.
server                                                   - Show running server info.
target                                                   - Displays current target information.
bind [host]                                              - Connects to the indicated available host.
disconnect                                               - Close all current connections and shut down the server. This is Equals to (exit or quit).
?[command]                                               - Muestra ayuda solo de los comandos anteriores
"""

""" ?[command] """
command_help_savefile = """
savefile [namefile]  - Save the indicated file in the current path.\n
Example: 
    savefile myFile.db
"""
command_help_sendfile = """
sendfile ["all"] [filepath] [newFileName (includes extension)]  - Send a file to the target.\n
Example:
    sendfile D:/Documents/myFile.txt newNameFile.txt         -  Send file to current host.
    sendfile all D:/Documents/myFile.txt newNameFile.txt     -  send a file to all available hosts.
    sendfile -l D:/Documents/myFile.txt newNameFile.txt      -  allows the entry of a list of hosts to send the file to them. 
"""
command_help_block    = "block [all or 'host' or 'hostlist']  - Blocks connections from indicated hosts. If is hostList separate with comma\n"
command_help_free     = "free [all or 'host' or 'hostlist']  - Releases connections from the indicated hosts. If is hostList separate with comma\n"
command_help_hosts    = "hosts  - Shows available and blocked hosts.\n"
command_help_server   = "server  - Show running server info.\n"
command_help_target   = "target  - Displays current target information.\n"
command_help_bind     = "bind [host]  - Connects to the indicated available host.\n"
command_help_exit     = "disconnect  - Close all current connections and shutdown the server. This is Equals to (exit or quit).\n"

def get_command_help(command):
    if command == "savefile":
        return command_help_savefile
    elif command == "sendfile":
        return command_help_sendfile
    elif command == "block":
        return command_help_block
    elif command == "free":
        return command_help_free
    elif command == "hosts":
        return command_help_hosts
    elif command == "server":
        return command_help_server
    elif command == "target":
        return command_help_target
    elif command == "bind":
        return command_help_bind
    elif command in ["exit", "disconnect", "quit"]:
        return command_help_exit
    else:
        return "[!] Command not found\n"