# Command_Packages/wc.py

from .dbCommands import DbCommands
from rich.text import Text
from rich.console import Console
from shell import get_CWD
import base64

db_path = './P01/ApiStarter/data/filesystem.db'

def wc(**kwargs):
    """
    NAME
       wc - print newline, word, and byte counts for each FILE

    SYNOPSIS
       wc [OPTION]... [FILE]...

    DESCRIPTION
       Print newline, word, and byte counts for each FILE.
    """
    
    # WC doesn't handle flags nor params
    flags = kwargs.get("flags")
    params = kwargs.get("params")
    
    cwd = get_CWD()
    count = 0
    lines = 0
    chars = 0
    console = Console()
    valid_flags = ["l", "m", "w"]
    string = ''
    newline = '\n'
    string = Text(string)
    newline = Text(newline)
    
    content = params[-1]
    
    size = len(content.encode('utf-8'))
    
    if size < 100:
        if "./P01" in content:
         # If looking in a local file 
            with open(content, 'r') as open_file:
                for line_number, line in enumerate(open_file, start=0):
                    lines += 1
                    for word in line:
                        if word != ' ' or word != '\n':
                            count += 1
                            for char in word:
                                chars += 1
                c_size = len(open_file.encode('utf-8'))
                
                if flags:
                    if len(flags) == 1:
                        flags = flags[0]
                        flags = flags.strip('-')
                        if flags in valid_flags:
                            if flags == 'l':
                                return(f'{lines}')
                            elif flags == 'm':
                                return(f'{chars}')
                            elif flags == 'w':
                                return(f'{count}')
                                                
                        else:
                            return(f'Only -l, -m, and -w are supported in this shell.')
                else:
                    return(f'Words: {count} Bytes: {c_size}')

        else:
            if "." in content:
                file_id, dir_id = DbCommands.get_file_and_dir_id(db_path, content)
            if DbCommands.file_exists(db_path, content, dir_id):
                file_contents = DbCommands.get_Content(db_path, file_id, dir_id)
                                                
                for line_number, line in enumerate(file_contents, start=0):
                    lines += 1
                    for word in line:
                        if word != ' ' or word != '\n':
                            count += 1
                            for char in word:
                                chars += 1
                c_size = len(file_contents.encode('utf-8'))
                
                if flags:
                    if len(flags) == 1:
                        flags = flags[0]
                        flags = flags.strip('-')
                        if flags in valid_flags:
                            if flags == 'l':
                                print("lines")
                                return(f'{lines}')
                            elif flags == 'm':
                                print("chars")
                                return(f'{chars}')
                            elif flags == 'w':
                                print("size")
                                return(f'{c_size}')
                                                
                        else:
                            return(f'Only -l, -m, and -w are supported in this shell.')
                else:
                    return(f'Words: {count} Bytes: {c_size}')
    