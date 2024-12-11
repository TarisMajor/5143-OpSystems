# Command_Packages/ls.py
from shell import get_CWD
from .dbCommands import DbCommands


db_path = './P01/ApiStarter/data/filesystem.db' 

def rmdir(**kwargs):
    """
    NAME
       rmdir - remove directory with all files associated

    SYNOPSIS
       mkdir [OPTION]... DIRECTORY...

    DESCRIPTION
       Create  the  DIRECTORY(ies),  if they do not already exist.

       Mandatory arguments to long options are mandatory for short options too.

        -p, --parents
              no error if existing, make parent directories as needed
    """
    
    flags = kwargs.get("flags")
    params = kwargs.get("params")
    
    cwd = get_CWD()
    
    name = params[0]
    
    if "/" in cwd:
        paths = cwd.split("/")
        paths = paths[1:]
        path = paths[-1]
        
    
    if flags:
        return(f'This function does not accept flags.')
    else:
        if DbCommands.dir_exists(db_path, name):
            dir = DbCommands.get_dir_id(db_path, name)
            result = DbCommands.remove_directory(db_path, name, dir)
            return(result)
            
        else:
            return(f'The directory already exists.')