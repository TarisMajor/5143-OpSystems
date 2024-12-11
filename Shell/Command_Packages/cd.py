# Command_Packages/cd.py
import shell
from shell import db_path
from .dbCommands import DbCommands

global cwd
global db_Path
default = "/1000-Spatial_Data_Structures"

def cd(**kwargs):
    cwd = shell.get_CWD()
    
    flags = kwargs.get("flags")
    params = kwargs.get("params")
    
    if params:
        directory = params[0]
        if ".." in directory:
            if cwd == default:
                return("You are already in the root directory.")
            else:
                cwd = cwd.split("/")
                cwd = cwd[:-1]
                cwd = "/".join(cwd)
                shell.modify_CWD(cwd)
        
        else:
            if DbCommands.dir_exists(db_path, directory):
                cwd = cwd + "/" + directory
                shell.modify_CWD(cwd)
            else:
                return("Directory does not exist.")
        
        shell.modify_CWD(cwd)
        return(cwd)
     
    else:
        shell.modify_CWD(default)
        return(default)
        
    