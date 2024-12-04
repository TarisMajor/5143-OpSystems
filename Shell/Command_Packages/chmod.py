from .dbCommands import DbCommands
from shell import cwd

db_path = './P01/ApiStarter/data/filesystem.db'  

def chmod(**kwargs):
    
    flags = kwargs.get("flags")
    params = kwargs.get("params")
    
    permissions = params[0]
    file_name = params[1]
    
    if "/" in cwd:
            params = cwd.split("/")
            params = params[1:]
            
        
    
    if flags:
        return(f"This function does not accept flags")
    else:
        for param in params:
            if param == params[-1]:
                if DbCommands.file_exists(db_path, file_name):
                    result = DbCommands.change_permissions(db_path, file_name,permissions)
                else:
                    result = (f"The file does not exist.")
            
    return(result)