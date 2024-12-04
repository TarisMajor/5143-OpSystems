# Command_Packages/ls.py
from shell import cwd
from shell import get_CWD
from .dbCommands import DbCommands


db_path = './P01/ApiStarter/data/filesystem.db'  


def ls(**kwargs):
    """
    NAME
       ls - list directory contents

    SYNOPSIS
       ls [OPTION]... [FILE]...

    DESCRIPTION
       List  information  about the FILEs (the current directory by default).  Sort entries alphabetically if none of
       -cftuvSUX nor --sort is specified.

       Mandatory arguments to long options are mandatory for short options too.

        -a, --all
              do not ignore entries starting with .
              
        -h, --human-readable
              with -l and -s, print sizes like 1K 234M 2G etc.
              
        -l     use a long listing format
    """
    
    flags = kwargs.get("flags")
    params = kwargs.get("params")
    
    valid_flags = ["l", "a", "h"]
            
    cwd = get_CWD()
    
    if "/" in cwd:
        paths = cwd.split("/")
        paths = paths[1:]
    
    if params:
        params_string = ''
        for param in params:
            params_string = params_string + param
            
        if "/" in params_string:    
            params = params_string.split("/")
            params = params[1:]
                
        for param in params:
            if param == params[-1]:
                if DbCommands.dir_exists(db_path, param):
                    dir_id = DbCommands.get_dir_id(db_path, param)
                    listing = DbCommands.get_listing(db_path, dir_id)
                else:
                    return("Directory does not exist.")
            
    else:
        if "/" in cwd:
            params = cwd.split("/")
            params = params[1:]
            
        for param in params:
            if param == params[-1]:
                if DbCommands.dir_exists(db_path, param):
                    dir_id = DbCommands.get_dir_id(db_path, param)
                    listing = DbCommands.get_listing(db_path, dir_id)
                else:
                    return("Directory does not exist.")
           
    if flags:
        name = paths[-1]
        flags = [flag[1:] for flag in flags]
        
        if len(flags) == 1:
            flags = list(flags[0])
            
        for flag in flags:
            if flag in valid_flags:
                dir_id = DbCommands.get_dir_id(db_path, name)
                listing = DbCommands.get_long_listing(db_path,dir_id, flags)
            else:
                return("Not a valid flag.")
            
    return listing