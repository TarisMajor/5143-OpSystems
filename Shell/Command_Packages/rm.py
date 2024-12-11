# Command_Packages/ls.py
from shell import get_CWD
from .dbCommands import DbCommands


db_path = './P01/ApiStarter/data/filesystem.db' 

def rm(**kwargs):
    
    """
    NAME
       rm - remove file

    SYNOPSIS
       rm [OPTION]... [FILE]...

    DESCRIPTION
       Remove (unlink) the FILE(s).

       Mandatory arguments to long options are mandatory for short options too.

    """
    
    flags = kwargs.get("flags")
    params = kwargs.get("params")
    
    cwd = get_CWD()
    
    name = params[0]
    
    if '.' in name:
        if DbCommands.this_file_exists(db_path, name):
            file_id, dir_id = DbCommands.get_file_and_dir_id(db_path, name)
            result = DbCommands.remove_file(db_path, name, dir_id)
            return(result)
        else:
            return(f'The file does not exist.')
    else:
        if DbCommands.dir_exists(db_path, name):
            dir_id = DbCommands.get_dir_id(db_path, name)
            result = DbCommands.remove_directory(db_path, name, dir_id)
            return(result)
        else:
            return(f'The directory does not exist.')
        