# Command_Packages/ls.py
from shell import get_CWD
from .dbCommands import DbCommands


db_path = './P01/ApiStarter/data/filesystem.db' 

def mkdir(**kwargs):
    """
    NAME
       mkdir - make directory

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
            return(f'The directory already exists.')
        else:
            dir = DbCommands.get_dir_id(db_path, path)
            print(dir)
            result = DbCommands.create_directory(db_path, name, dir)
            return(result)