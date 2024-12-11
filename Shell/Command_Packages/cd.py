# Command_Packages/cd.py
from shell import modify_CWD
from shell import get_CWD
from shell import db_path
from .dbCommands import DbCommands

global cwd
global db_Path

default = "/1000-Spatial_Data_Structures"

def cd(**kwargs):
    
    cwd = get_CWD()
    
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
                modify_CWD(cwd)
        
        else:
            if DbCommands.dir_exists(db_path, directory):
                cwd = cwd + "/" + directory
                modify_CWD(cwd)
            else:
                return("Directory does not exist.")
                
        return(cwd)
     
    else:
        modify_CWD(default)
        return(default)
        
    