from .dbCommands import DbCommands
from shell import get_CWD

db_path = './P01/ApiStarter/data/filesystem.db'  

def chmod(**kwargs):
    
    flags = kwargs.get("flags")
    params = kwargs.get("params")
    
    permissions = params[0]
    name = params[1]
                
    if flags:
        return(f"This function does not accept flags")
    else:
        if "." in name:
            file_id, dir_id = DbCommands.get_file_and_dir_id(db_path, name)
            if DbCommands.file_exists(db_path, name, dir_id):
                
                result = DbCommands.change_permissions(db_path, name,permissions)
            else:
                result = (f"The file does not exist.")
        else:
            if DbCommands.dir_exists(db_path, name):
                result = DbCommands.change_directory_permissions(db_path, name,permissions)
            else:
                result = (f"The directory does not exist.")
            
    return(result)