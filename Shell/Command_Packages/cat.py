#!/usr/bin/env python
from subprocess import call
from .dbCommands import DbCommands
from shell import get_CWD

db_path = './P01/ApiStarter/data/filesystem.db'  

def cat(**kwargs):
    """   
    NAME
        cat - concatenate files and print on the standard output
    SYNOPSIS
        cat [OPTION]... [FILE]...
    DESCRIPTION
        Concatenate FILE(s) to standard output.

    """
    flags = kwargs.get("flags")
    params = kwargs.get("params")
    
    string = ''
        
    if flags:
        return(f"This function does not accept flags")
    else:
        for param in params:
            if "." in param:
                if DbCommands.this_file_exists(db_path, param):
                    file_id, dir_id = DbCommands.get_file_and_dir_id(db_path, param)
                    file_contents = DbCommands.get_Content(db_path, file_id, dir_id)
            
                    string += file_contents + "\n"
                else:
                    return(f"The file does not exist.")
            
    return(string)