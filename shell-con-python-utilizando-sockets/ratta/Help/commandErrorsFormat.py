
free_error_format = """
[-] ERROR Format: free <IP> or free <id> or free all
    examples: by ip ----------> free 192.168.1.67, 192.233.43.26, 34.678.234.89
              by id ----------> free 3,4,2,6
              by id sequence -> free 1-9\n
"""

block_error_format = """
[-] ERROR Format: block <IP> or block <id> or block all
    examples: by ip ----------> block 192.168.1.67, 192.233.43.26, 34.678.234.89
              by id ----------> block 3,4,2,6
              by id sequence -> block 1-9\n
"""

sendFile_error_format = """
[!] FORMAT ERROR:
        1.- Path file does not exist
        2.- Or the file extension is wrong!!
    Example:
        -> sendfile C:\\Users\\Admin\\Documents\\great.txt NewFileName.txt
"""